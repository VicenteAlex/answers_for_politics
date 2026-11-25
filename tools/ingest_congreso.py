#!/usr/bin/env python3
"""Build votes / vote_results / parliamentary_groups / initiatives for the Congreso from raw/congreso/ (see congreso_download.py).

Usage: .venv/Scripts/python tools/ingest_congreso.py [--leg XIV XV]

Party attribution (votes are recorded per deputy and parliamentary group, not per party):
  1. tools/congreso_party_map.csv: explicit deputy -> party for deputies of multi-party groups (Mixto, Plural...), with source.
  2. XV only: the deputy's FORMACIONELECTORAL from the deputies open data (candidacy) when the group is multi-party.
  3. Otherwise GROUP_PARTY below (single-party groups). PSC deputies sit in the Socialist group and are counted as es-psoe.
  Deputies that cannot be attributed get party_id empty (they still count in their group).
Files written (owned by this script, fully rewritten): data/es/votes/<leg>.csv, data/es/vote_results/<leg>.csv,
data/es/initiatives/<leg>.csv; parliamentary_groups rows with this script's ids are upserted.
"""
from __future__ import annotations

import argparse
import collections
import csv
import datetime as dt
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw" / "congreso"
DATA = ROOT / "data" / "es"
MAP_FILE = ROOT / "tools" / "congreso_party_map.csv"
for _s in (sys.stdout, sys.stderr):
    _s.reconfigure(encoding="utf-8", errors="replace")

LEG_ID = {"XIV": "es-leg-xiv", "XV": "es-leg-xv"}
# group code in the votes JSON -> (group name, default party or None if multi-party)
GROUPS = {
    "XIV": {"GS": ("Grupo Parlamentario Socialista", "es-psoe"), "GP": ("Grupo Parlamentario Popular", "es-pp"),
            "GVOX": ("Grupo Parlamentario VOX", "es-vox"),
            "GCUP-EC-GC": ("Grupo Parlamentario Confederal de Unidas Podemos-En Comú Podem-Galicia en Común", "es-up"),
            "GR": ("Grupo Parlamentario Republicano", "es-erc"), "GCs": ("Grupo Parlamentario Ciudadanos", "es-cs"),
            "GV": ("Grupo Parlamentario Vasco (EAJ-PNV)", "es-pnv"), "GEH": ("Grupo Parlamentario Euskal Herria Bildu", "es-eh-bildu"),
            "GPlu": ("Grupo Parlamentario Plural", None), "GMx": ("Grupo Parlamentario Mixto", None)},
    "XV": {"GS": ("Grupo Parlamentario Socialista", "es-psoe"), "GP": ("Grupo Parlamentario Popular en el Congreso", "es-pp"),
           "GVOX": ("Grupo Parlamentario VOX", "es-vox"), "GSUMAR": ("Grupo Parlamentario Plurinacional SUMAR", "es-sumar"),
           "GR": ("Grupo Parlamentario Republicano", "es-erc"), "GJxCAT": ("Grupo Parlamentario Junts per Catalunya", "es-junts"),
           "GEH": ("Grupo Parlamentario Euskal Herria Bildu", "es-eh-bildu"), "GV": ("Grupo Parlamentario Vasco (EAJ-PNV)", "es-pnv"),
           "GMx": ("Grupo Parlamentario Mixto", None)},
}
FORMACION_PARTY = {"BNG": "es-bng", "CCa": "es-cc", "CC": "es-cc", "UPN": "es-upn", "PSOE": "es-psoe", "PSC-PSOE": "es-psc",
                   "PP": "es-pp", "VOX": "es-vox", "SUMAR": "es-sumar", "ERC": "es-erc", "JxCAT-JUNTS": "es-junts",
                   "EH Bildu": "es-eh-bildu", "EAJ-PNV": "es-pnv"}
VOTE = {"Sí": "yes", "No": "no", "Abstención": "abstain", "No vota": "absent"}


def norm(s: str) -> str:
    s = "".join(c for c in unicodedata.normalize("NFKD", s or "") if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s).strip().lower()


def slug(s: str, n: int = 40) -> str:
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", norm(s))).strip("-")[:n].strip("-")


def classify(info: dict) -> str:
    t = norm(" ".join(str(info.get(k) or "") for k in ("titulo", "textoExpediente", "tituloSubGrupo", "textoSubGrupo")))
    ti = norm(info.get("titulo") or "")
    if "investidura" in t:
        return "investiture"
    if "mocion de censura" in t:
        return "motion_of_censure"
    if "convalidacion o derogacion" in t or "convalidacion de real decreto" in t:
        return "decree_as_bill" if "tramitacion como proyecto" in t else "decree_validation"
    if "totalidad" in t:
        return "totality_amendment"
    if "toma en consideracion" in t:
        return "taken_into_consideration"
    if "votacion de conjunto" in t or "votacion final" in t:
        return "final_vote"
    if "proposiciones no de ley" in ti or "proposicion no de ley" in t:
        return "non_legislative_motion"
    if "mociones consecuencia" in ti or "mocion consecuencia" in t:
        return "motion"
    if "presupuestos generales" in t and "totalidad" not in t:
        return "budget" if "enmienda" not in t else "amendment"
    if "enmienda" in t or "enmiendas" in t:
        return "amendment"
    if "dictamen" in ti or "dictamenes" in ti:
        return "final_vote"
    return "other"


def load_map() -> dict:
    out = collections.defaultdict(list)
    if MAP_FILE.exists():
        for r in csv.DictReader(MAP_FILE.open(encoding="utf-8")):
            out[(r["legislature"], norm(r["deputy"]))].append(r)
    return out


def load_formaciones() -> dict:
    out = {}
    for f in ("DiputadosActivos.json", "DiputadosDeBaja.json"):
        p = RAW / "diputados" / f
        if p.exists():
            for r in json.loads(p.read_text(encoding="utf-8-sig")):
                out[norm(r["NOMBRE"])] = r.get("FORMACIONELECTORAL")
    return out


def party_for(leg, deputy, group, day, pmap, formaciones, unmapped):
    for r in pmap.get((leg, norm(deputy)), []):
        if (not r["valid_from"] or r["valid_from"] <= day) and (not r["valid_to"] or day <= r["valid_to"]):
            return r["party_id"] or None
    name, default = GROUPS[leg].get(group, (group, None))
    if default:
        return default
    if leg == "XV":
        f = formaciones.get(norm(deputy))
        if f in FORMACION_PARTY and FORMACION_PARTY[f] != "es-sumar":
            return FORMACION_PARTY[f]
    unmapped[(leg, deputy, group)] += 1
    return None


def write_csv(path: Path, header: list[str], rows: list[dict]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=header, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({h: ("" if r.get(h) is None else ("true" if r.get(h) is True else "false" if r.get(h) is False else r.get(h))) for h in header})


def ingest_leg(leg: str, pmap, formaciones, unmapped):
    votes, results = [], []
    seen_groups = set()
    files = sorted((RAW / "votaciones" / leg).glob("*/Votacion*/*.json"))
    for f in files:
        d = json.loads(f.read_text(encoding="utf-8-sig"))
        info, tot = d["informacion"], d["totales"]
        day = dt.datetime.strptime(info["fecha"], "%d/%m/%Y").date().isoformat()
        n = int(info["numeroVotacion"])
        vote_id = f"es-vote-{leg.lower()}-{day}-s{int(info['sesion']):03d}-v{n:03d}"
        obj = classify(info)
        yes, no, abst = int(tot.get("afavor") or 0), int(tot.get("enContra") or 0), int(tot.get("abstenciones") or 0)
        absent = int(tot.get("noVotan") or 0)
        if str(tot.get("asentimiento", "No")).lower().startswith("s"):
            result = "approved"
        elif yes > no:
            result = "approved"
        elif yes < no:
            result = "rejected"
        else:
            result = "tied"
        title_parts = [info.get("textoExpediente"), info.get("tituloSubGrupo"), info.get("textoSubGrupo")]
        title = " | ".join(re.sub(r"\s+", " ", p).strip() for p in title_parts if p and p.strip()) or info.get("titulo", "")
        votes.append(dict(vote_id=vote_id, jurisdiction_id="es", chamber="congreso", legislature_id=LEG_ID[leg], date=day,
                          session=str(info["sesion"]), vote_number=n, object=obj, bundled=False,
                          title=(re.sub(r"\s+", " ", info.get("titulo", "")).strip() + " — " + title)[:600],
                          result=result, yes=yes, no=no, abstain=abst, absent=absent,
                          url=("https://www.congreso.es/es/opendata/votaciones?p_p_id=votaciones&p_p_lifecycle=0&p_p_state=normal"
                               f"&p_p_mode=view&targetLegislatura={leg}&targetDate={day[8:]}/{day[5:7]}/{day[:4]}")))
        agg = collections.defaultdict(lambda: collections.Counter())
        for v in d.get("votaciones", []):
            grp = v.get("grupo") or ""
            seen_groups.add(grp)
            party = party_for(leg, v["diputado"], grp, day, pmap, formaciones, unmapped)
            agg[(grp, party)][VOTE.get(v.get("voto"), "absent")] += 1
        for (grp, party), c in agg.items():
            results.append(dict(vote_id=vote_id, group_id=f"es-group-{leg.lower()}-{slug(grp, 20)}" if grp else None,
                                party_id=party, yes=c["yes"], no=c["no"], abstain=c["abstain"], absent=c["absent"]))
    # vote ids must be unique (repeated votes in a session keep the number from the file)
    dup = [k for k, n in collections.Counter(v["vote_id"] for v in votes).items() if n > 1]
    if dup:
        print(f"WARNING {leg}: {len(dup)} duplicate vote ids, e.g. {dup[:3]}", file=sys.stderr)
    return votes, results, seen_groups


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--leg", nargs="+", default=["XIV", "XV"])
    args = ap.parse_args()
    pmap, formaciones = load_map(), load_formaciones()
    unmapped = collections.Counter()
    vote_cols = ["vote_id", "jurisdiction_id", "chamber", "legislature_id", "date", "session", "vote_number", "initiative_id",
                 "object", "bundled", "title", "result", "yes", "no", "abstain", "absent", "url"]
    res_cols = ["vote_id", "group_id", "party_id", "yes", "no", "abstain", "absent"]
    groups = []
    for leg in args.leg:
        votes, results, seen = ingest_leg(leg, pmap, formaciones, unmapped)
        write_csv(DATA / "votes" / f"{LEG_ID[leg]}.csv", vote_cols, votes)
        write_csv(DATA / "vote_results" / f"{LEG_ID[leg]}.csv", res_cols, results)
        for code in sorted(c for c in seen if c):
            name = GROUPS[leg].get(code, (code, None))[0]
            groups.append(dict(group_id=f"es-group-{leg.lower()}-{slug(code, 20)}", chamber="congreso", jurisdiction_id="es",
                               legislature_id=LEG_ID[leg], name=name, abbreviation=code))
        print(f"{leg}: {len(votes)} votes, {len(results)} result rows, groups {sorted(seen)}")
    # upsert groups
    gpath = DATA / "parliamentary_groups.csv"
    with gpath.open(encoding="utf-8-sig", newline="") as f:
        r = csv.DictReader(f)
        header, rows = r.fieldnames, {x["group_id"]: x for x in r}
    for g in groups:
        rows[g["group_id"]] = {h: g.get(h, "") for h in header}
    write_csv(gpath, header, [rows[k] for k in sorted(rows)])
    if unmapped:
        print(f"unattributed deputies (party empty): {len(unmapped)}")
        for (leg, dep, grp), n in sorted(unmapped.items()):
            print(f"  {leg} {grp:6} {dep} ({n} votes)")


if __name__ == "__main__":
    main()

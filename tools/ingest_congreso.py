#!/usr/bin/env python3
"""Build votes / vote_casts / parliamentary_groups / initiatives for the Congreso from raw/congreso/ (see congreso_download.py).

Usage: .venv/Scripts/python tools/ingest_congreso.py [--leg XIV XV]

Party attribution (votes are recorded per deputy and parliamentary group, not per party):
  1. tools/congreso_party_map.csv: explicit deputy -> party for deputies of multi-party groups (Mixto, Plural...), with source.
  2. XV only: the deputy's FORMACIONELECTORAL from the deputies open data (candidacy) when the group is multi-party.
  3. Otherwise GROUP_PARTY below (single-party groups). PSC deputies sit in the Socialist group and are counted as es-psoe.
  Deputies that cannot be attributed get party_id empty (they still count in their group).
Files written (owned by this script, fully rewritten): data/es/votes/<leg>.csv, data/es/vote_casts/<leg>/<date>.parquet,
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
            "GV (EAJ-PNV)": ("Grupo Parlamentario Vasco (EAJ-PNV)", "es-pnv"), "GEH Bildu": ("Grupo Parlamentario Euskal Herria Bildu", "es-eh-bildu"),
            "GPlu": ("Grupo Parlamentario Plural", None), "GMx": ("Grupo Parlamentario Mixto", None)},
    "XV": {"GS": ("Grupo Parlamentario Socialista", "es-psoe"), "GP": ("Grupo Parlamentario Popular en el Congreso", "es-pp"),
           "GVOX": ("Grupo Parlamentario VOX", "es-vox"), "GSUMAR": ("Grupo Parlamentario Plurinacional SUMAR", "es-sumar"),
           "GR": ("Grupo Parlamentario Republicano", "es-erc"), "GJxCAT": ("Grupo Parlamentario Junts per Catalunya", "es-junts"),
           "GEH Bildu": ("Grupo Parlamentario Euskal Herria Bildu", "es-eh-bildu"), "GV (EAJ-PNV)": ("Grupo Parlamentario Vasco (EAJ-PNV)", "es-pnv"),
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
    if "presupuestos generales" in t and "totalidad" not in t:
        return "budget" if "enmienda" not in t else "amendment"
    if "correccion tecnica" in t or "avocacion" in t:
        return "other"
    if "votacion de conjunto" in t or "votacion final" in t or "votacion del dictamen" in t:
        return "final_vote"
    if "proposiciones no de ley" in ti or "proposicion no de ley" in t:
        return "non_legislative_motion"
    if "mociones consecuencia" in ti or "mocion consecuencia" in t:
        return "motion"
    if "enmienda" in t or "enmiendas" in t:
        return "amendment"
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


def ingest_leg(leg: str, pmap, formaciones, unmapped, casts_writer, init_index=None):
    votes, results = [], []
    seen_groups = set()
    files = sorted((RAW / "votaciones" / leg).glob("*/Votacion*/*.json"))
    usual = collections.defaultdict(collections.Counter)  # deputy -> group counts (to attribute votes with empty group)
    for f in files:
        for v in json.loads(f.read_text(encoding="utf-8-sig")).get("votaciones", []):
            if v.get("grupo"):
                usual[v["diputado"]][v["grupo"]] += 1
    for f in files:
        d = json.loads(f.read_text(encoding="utf-8-sig"))
        info, tot = d["informacion"], d["totales"]
        day = dt.datetime.strptime(info["fecha"], "%d/%m/%Y").date().isoformat()
        retrieved = dt.date.fromtimestamp(f.stat().st_mtime).isoformat()
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
                               f"&p_p_mode=view&targetLegislatura={leg}&targetDate={day[8:]}/{day[5:7]}/{day[:4]}"),
                          source_file=f.name, retrieved=retrieved,
                          initiative_id=(init_index or {}).get(title_key(info.get("textoExpediente") or ""))))
        agg = collections.defaultdict(lambda: collections.Counter())
        for v in d.get("votaciones", []):
            grp = v.get("grupo") or ""
            seen_groups.add(grp)
            inferred = grp or (usual[v["diputado"]].most_common(1)[0][0] if usual[v["diputado"]] else "")
            party = party_for(leg, v["diputado"], inferred, day, pmap, formaciones, unmapped)
            vote = VOTE.get(v.get("voto"), "absent")
            agg[(grp, party)][vote] += 1
            casts_writer.writerow([day, vote_id, v.get("asiento") or "", v["diputado"],
                                   f"es-group-{leg.lower()}-{slug(grp, 20)}" if grp else "", party or "", vote])
        for (grp, party), c in agg.items():
            results.append(dict(vote_id=vote_id, group_id=f"es-group-{leg.lower()}-{slug(grp, 20)}" if grp else None,
                                party_id=party, yes=c["yes"], no=c["no"], abstain=c["abstain"], absent=c["absent"]))
    # vote ids must be unique (repeated votes in a session keep the number from the file)
    dup = [k for k, n in collections.Counter(v["vote_id"] for v in votes).items() if n > 1]
    if dup:
        print(f"WARNING {leg}: {len(dup)} duplicate vote ids, e.g. {dup[:3]}", file=sys.stderr)
    return votes, results, seen_groups


AUTHOR_PARTY = [("Socialista", "es-psoe"), ("Popular", "es-pp"), ("VOX", "es-vox"), ("SUMAR", "es-sumar"),
                ("Republicano", "es-erc"), ("Junts", "es-junts"), ("Euskal Herria Bildu", "es-eh-bildu"), ("Vasco", "es-pnv")]


def title_key(s: str) -> str:
    """Matching key between a vote's expediente text and an initiative title: drops the proposing groups
    ("del Grupo Parlamentario VOX, ...") and the word "orgánica", which the two sources place differently."""
    s = re.sub(r"\s(?:del|de los) Grupos? Parlamentarios? .*?,\s(?=[a-záéíóúñ]|Org[aá]nica)", " ", s or "")
    k = re.sub(r"[^a-z0-9]+", " ", norm(s))
    k = re.sub(r"\borganica\b", " ", k)
    return re.sub(r"\s+", " ", k).strip()[:100]


def ingest_initiatives() -> dict:
    """XV legislative initiatives (bills) from the open-data lists; returns title_key -> initiative_id for vote linking.
    The open data only lists the current legislature, so XIV initiatives are not available here."""
    rows, actors, index = [], [], {}
    for fname, default_type in (("ProyectosDeLey.json", "government_bill"), ("ProposicionesDeLey.json", "parliamentary_bill")):
        p = RAW / "iniciativas" / fname
        if not p.exists():
            continue
        for r in json.loads(p.read_text(encoding="utf-8-sig")):
            exp = (r.get("NUMEXPEDIENTE") or "").split("/")
            if len(exp) < 2:
                continue
            iid = f"es-init-xv-{exp[0]}-{exp[1]}"
            tipo = norm(r.get("TIPO", ""))
            itype = ("popular_initiative" if "iniciativa popular" in tipo else
                     default_type if ("proyecto" in tipo or "grupos parlamentarios" in tipo or "diputados" in tipo) else "other")
            res = (r.get("RESULTADOTRAMITACION") or "").strip()
            first = norm(res.split("\n")[0])
            status = ("approved" if first.startswith("aprobado") else "expired" if first.startswith(("caducado", "decaido"))
                      else "rejected" if first.startswith(("rechazado", "inadmitido")) else "withdrawn" if first.startswith("retirado")
                      else "other" if first else "in_progress")
            m = re.search(r"(\d{2})/(\d{2})/(\d{4})", res)
            title = re.sub(r"\s+", " ", r.get("OBJETO") or "").strip()
            rows.append(dict(initiative_id=iid, jurisdiction_id="es", chamber="congreso", legislature_id="es-leg-xv",
                             official_ref=r.get("NUMEXPEDIENTE"), initiative_type=itype, binding=True, title=title,
                             date_registered=dt.datetime.strptime(r["FECHAPRESENTACION"], "%d/%m/%Y").date().isoformat(),
                             status=status, status_date=f"{m.group(3)}-{m.group(2)}-{m.group(1)}" if m else None,
                             url="https://www.congreso.es/es/opendata/iniciativas"))
            index.setdefault(title_key(title), iid)
            for autor in (r.get("AUTOR") or "").split("\n"):
                for needle, party in AUTHOR_PARTY:
                    if needle in autor and "Grupo Parlamentario" in autor:
                        actors.append(dict(entity_id=iid, party_id=party, role="author"))
                        break
    cols = ["initiative_id", "jurisdiction_id", "chamber", "legislature_id", "official_ref", "initiative_type", "binding",
            "title", "date_registered", "status", "status_date", "url"]
    write_csv(DATA / "initiatives" / "es-leg-xv.csv", cols, rows)
    uniq = {(a["entity_id"], a["party_id"], a["role"]): a for a in actors}
    write_csv(DATA / "links" / "entity_actors__congreso.csv", ["entity_id", "party_id", "role"], list(uniq.values()))
    print(f"initiatives XV: {len(rows)} ({len(uniq)} author links)")
    return index, {r['initiative_id']: r['title'] for r in rows}


TOPIC_RULES = [  # (regex on normalised title, topic_id); keyword tagging = elaboración propia, review before relying on it
    (r"vivienda|alquiler|arrendamiento|desahucio", "housing"),
    (r"alquiler|arrendamientos urbanos|zonas? tensionad|contencion de rentas", "rent_regulation"),
    (r"alquiler turistico|viviendas? de uso turistico|pisos turisticos", "tourist_rentals"),
    (r"extranjer|inmigra|migratori|migrantes|asilo|proteccion internacional|regularizacion|arraigo", "immigration"),
    (r"menores (extranjeros|migrantes) no acompanados|menores migrantes|contingencia migratoria", "unaccompanied_minors"),
    (r"regularizacion extraordinaria", "regularization"),
    (r"impuesto|tributari|fiscal|gravamen|gravamenes", "taxation"),
    (r"impuesto sobre el patrimonio|grandes fortunas|solidaridad de las grandes", "wealth_tax"),
    (r"renta de las personas fisicas|irpf", "income_tax"),
    (r"sucesiones y donaciones", "inheritance_tax"),
    (r"impuesto sobre sociedades", "corporate_tax"),
    (r"pensiones|pensionistas|seguridad social", "pensions"),
    (r"salario minimo", "minimum_wage"),
    (r"estatuto de los trabajadores|reforma laboral|jornada|despido|contratacion laboral", "labor_regulation"),
    (r"presupuestos generales|estabilidad presupuestaria|deuda publica|techo de gasto", "public_finance"),
    (r"amnistia", "amnesty"),
    (r"financiacion autonomica|condonacion de (la )?deuda autonomica|fondo de liquidez autonomico", "regional_financing"),
    (r"sanidad|sanitari|salud publica", "health"),
    (r"educacion|educativ|universidad", "education"),
    (r"dependencia", "long_term_care"),
    (r"ingreso minimo vital|prestacion", "social_benefits"),
    (r"energ|electric|gas natural", "energy"),
    (r"cambio climatico|transicion ecologica|emisiones", "climate"),
    (r"igualdad|violencia de genero|violencia sexual|libertad sexual|paritaria", "gender_equality"),
    (r"memoria democratica|memoria historica", "historical_memory"),
    (r"corrupcion|financiacion ilegal|malversacion", "corruption"),
    (r"poder judicial|tribunal constitucional|consejo general del poder judicial|fiscal general", "judiciary"),
    (r"regimen electoral|ley electoral|loreg", "electoral_system"),
    (r"estado de alarma|emergencia|dana|catastrofe|incendios", "emergencies"),
    (r"defensa nacional|fuerzas armadas|gasto en defensa", "defense"),
    (r"estado de alarma|covid|pandemia", "health"),
]


def tag_topics(votes: list[dict], initiatives_titles: dict):
    """Keyword topic tags for votes and initiatives -> data/es/links/entity_topics__congreso.csv (owned by this script)."""
    rows = set()
    items = [(v["vote_id"], v["title"]) for v in votes] + list(initiatives_titles.items())
    for eid, title in items:
        t = norm(title)
        for pattern, topic in TOPIC_RULES:
            if re.search(pattern, t):
                rows.add((eid, topic))
    write_csv(DATA / "links" / "entity_topics__congreso.csv", ["entity_id", "topic_id"],
              [dict(entity_id=e, topic_id=t) for e, t in sorted(rows)])
    print(f"topic tags: {len(rows)} rows")


def write_casts_parquet(leg: str, tmp_csv: Path):
    """One zstd parquet file per voting day (append-friendly for git); the folder is owned by this script."""
    import duckdb
    out_dir = DATA / "vote_casts" / LEG_ID[leg]
    if out_dir.exists():
        for old in out_dir.glob("*.parquet"):
            old.unlink()
    out_dir.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect()
    con.execute(f"CREATE TABLE c AS SELECT * FROM read_csv('{tmp_csv.as_posix()}', header=true, all_varchar=true)")
    for (day,) in con.execute("SELECT DISTINCT date FROM c ORDER BY 1").fetchall():
        dest = (out_dir / f"{day}.parquet").as_posix()
        con.execute(f"COPY (SELECT vote_id, NULLIF(seat, '') AS seat, deputy, NULLIF(group_id, '') AS group_id, "
                    f"NULLIF(party_id, '') AS party_id, vote FROM c WHERE date = ? ORDER BY vote_id, deputy) "
                    f"TO '{dest}' (FORMAT parquet, COMPRESSION zstd)", [day])
    con.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--leg", nargs="+", default=["XIV", "XV"])
    args = ap.parse_args()
    pmap, formaciones = load_map(), load_formaciones()
    unmapped = collections.Counter()
    vote_cols = ["vote_id", "jurisdiction_id", "chamber", "legislature_id", "date", "session", "vote_number", "initiative_id",
                 "object", "bundled", "title", "result", "yes", "no", "abstain", "absent", "url", "source_file", "retrieved"]
    groups = []
    init_index, init_titles = ingest_initiatives()
    all_votes = []
    for leg in args.leg:
        tmp = ROOT / "build" / f"casts_{leg}.csv"
        tmp.parent.mkdir(parents=True, exist_ok=True)
        with tmp.open("w", encoding="utf-8", newline="") as fh:
            cw = csv.writer(fh, lineterminator="\n")
            cw.writerow(["date", "vote_id", "seat", "deputy", "group_id", "party_id", "vote"])
            votes, results, seen = ingest_leg(leg, pmap, formaciones, unmapped, cw, init_index if leg == "XV" else None)
        write_csv(DATA / "votes" / f"{LEG_ID[leg]}.csv", vote_cols, votes)
        all_votes += votes
        write_casts_parquet(leg, tmp)
        tmp.unlink()
        for code in sorted(c for c in seen if c):
            name = GROUPS[leg].get(code, (code, None))[0]
            groups.append(dict(group_id=f"es-group-{leg.lower()}-{slug(code, 20)}", chamber="congreso", jurisdiction_id="es",
                               legislature_id=LEG_ID[leg], name=name, abbreviation=code))
        print(f"{leg}: {len(votes)} votes, groups {sorted(seen)}")
    tag_topics(all_votes, init_titles)
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

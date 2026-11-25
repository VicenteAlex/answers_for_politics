#!/usr/bin/env python3
"""Ingest statistical indicators for Spain from the INE and Eurostat APIs.

Usage (repo root):
  .venv/Scripts/python tools/ingest_indicators.py            # all indicators (Windows; .venv/bin/python elsewhere)
  .venv/Scripts/python tools/ingest_indicators.py --only es-unemployment-rate es-gini
  .venv/Scripts/python tools/ingest_indicators.py --list

Writes data/es/indicators/<indicator_id>.csv (whole file, owned by this script), upserts the matching rows of
data/es/indicator_defs.csv and the 'es-cov-indicators' row of data/es/coverage.csv.
To add an indicator, add a spec to SPECS (INE: table id + regex on series names; Eurostat: dataset + filters).
"""
from __future__ import annotations

import argparse
import calendar
import csv
import datetime as dt
import json
import re
import ssl
import sys
import time
import unicodedata
import urllib.request
from pathlib import Path

import truststore  # OS certificate store (Eurostat's chain fails with Python's bundled defaults on Windows)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "es"
SSL_CTX = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
INE_TABLE = "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/{table}?tip=A"
EUROSTAT = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/{dataset}?format=JSON&lang=EN"

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")


def norm(s: str) -> str:
    s = "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", s.lower())


CCAA = {norm(k): v for k, v in {
    "Total Nacional": "es", "Nacional": "es", "Andalucía": "es-an", "Aragón": "es-ar",
    "Asturias, Principado de": "es-as", "Balears, Illes": "es-ib", "Canarias": "es-cn", "Cantabria": "es-cb",
    "Castilla y León": "es-cl", "Castilla - La Mancha": "es-cm", "Cataluña": "es-ct", "Comunitat Valenciana": "es-vc",
    "Extremadura": "es-ex", "Galicia": "es-ga", "Madrid, Comunidad de": "es-md", "Murcia, Región de": "es-mc",
    "Navarra, Comunidad Foral de": "es-nc", "País Vasco": "es-pv", "Rioja, La": "es-ri", "Ceuta": "es-ce",
    "Melilla": "es-ml"}.items()}
MUNICIPALITIES = {norm("Barcelona"): "es-ct-08019", norm("Madrid"): "es-md-28079"}

# --------------------------------------------------------------------------------------------- indicator specs
R = r"(?P<region>[^.]+)"
SPECS = [
    # ---- INE: labour market (EPA, quarterly)
    dict(id="es-unemployment-rate", source="ine", unit="%", frequency="quarterly", real="not_applicable", sa=False,
         name_es="Tasa de paro (EPA)", name_en="Unemployment rate (Labour Force Survey)",
         notes="Población de 16 y más años, ambos sexos. Nacional y CCAA.",
         pulls=[dict(table=65334, pattern=rf"^Tasa de paro de la población\. Ambos sexos\. {R}\. Total\.$", regions=CCAA)]),
    dict(id="es-youth-unemployment-rate", source="ine", unit="%", frequency="quarterly", real="not_applicable", sa=False,
         name_es="Tasa de paro de menores de 25 años (EPA)", name_en="Youth (<25) unemployment rate (LFS)",
         notes="Ambos sexos. Nacional y CCAA.",
         pulls=[dict(table=65334, pattern=rf"^Tasa de paro de la población\. Ambos sexos\. {R}\. Menores de 25 años\.$", regions=CCAA)]),
    dict(id="es-unemployment-rate-spanish", source="ine", unit="%", frequency="quarterly", real="not_applicable", sa=False,
         name_es="Tasa de paro de la población de nacionalidad española (EPA)", name_en="Unemployment rate, Spanish nationals (LFS)",
         notes="Por nacionalidad, no por país de nacimiento. Nacional y CCAA.",
         pulls=[dict(table=65336, pattern=rf"^Tasa de paro de la población\. Ambos sexos\. {R}\. Española\.$", regions=CCAA)]),
    dict(id="es-unemployment-rate-foreign", source="ine", unit="%", frequency="quarterly", real="not_applicable", sa=False,
         name_es="Tasa de paro de la población de nacionalidad extranjera (EPA)", name_en="Unemployment rate, foreign nationals (LFS)",
         notes="Por nacionalidad, no por país de nacimiento. Nacional y CCAA.",
         pulls=[dict(table=65336, pattern=rf"^Tasa de paro de la población\. Ambos sexos\. {R}\. Extranjera: Total\.$", regions=CCAA)]),
    dict(id="es-unemployment-rate-foreign-non-eu", source="ine", unit="%", frequency="quarterly", real="not_applicable", sa=False,
         name_es="Tasa de paro de extranjeros no pertenecientes a la UE (EPA)", name_en="Unemployment rate, non-EU foreign nationals (LFS)",
         notes="Por nacionalidad. Nacional y CCAA.",
         pulls=[dict(table=65336, pattern=rf"^Tasa de paro de la población\. Ambos sexos\. {R}\. Extranjera: No pertenecientes a la Unión Europea\.$", regions=CCAA)]),
    # ---- INE: prices
    dict(id="es-cpi-annual-rate", source="ine", unit="%", frequency="monthly", real="not_applicable", sa=False,
         name_es="IPC general: variación anual", name_en="CPI, all items: annual rate of change",
         notes="Índice general nacional, serie desde 1961.",
         pulls=[dict(table=76134, pattern=r"^Nacional\. Índice general\. Variación anual\.$", default_region="es")]),
    dict(id="es-house-price-index", source="ine", unit="índice", frequency="quarterly", real="nominal", sa=False,
         name_es="Índice de Precios de Vivienda (IPV): general", name_en="House Price Index (HPI): all dwellings",
         notes="Vivienda libre nueva y de segunda mano, transacciones. Nacional y CCAA. Ver base en INE.",
         pulls=[dict(table=80270, pattern=rf"^{R}\. General\. Índice\.$", regions=CCAA)]),
    dict(id="es-house-price-annual-change", source="ine", unit="%", frequency="quarterly", real="nominal", sa=False,
         name_es="IPV general: variación anual", name_en="House Price Index: annual rate of change",
         notes="Nacional y CCAA.",
         pulls=[dict(table=80270, pattern=rf"^{R}\. General\. Variación anual\.$", regions=CCAA)]),
    dict(id="es-rent-price-index", source="ine", unit="índice (2015=100)", frequency="annual", real="nominal", sa=False,
         name_es="Índice de Precios de Vivienda en Alquiler (IPVA): total", name_en="Housing Rental Price Index (experimental): total",
         notes="Estadística experimental a partir de declaraciones de IRPF (contratos vigentes, no solo nuevos). Nacional, CCAA y municipios de Barcelona y Madrid. Publicación con retraso de más de un año.",
         pulls=[dict(table=59056, pattern=rf"^{R}\. Total\. Índice\.$", regions=CCAA),
                dict(table=59060, pattern=rf"^{R}\. Índice\. Total\.$", regions=MUNICIPALITIES)]),
    dict(id="es-rent-price-annual-change", source="ine", unit="%", frequency="annual", real="nominal", sa=False,
         name_es="IPVA total: variación anual", name_en="Housing Rental Price Index: annual rate of change",
         notes="Estadística experimental (IRPF; contratos vigentes). Nacional, CCAA y municipios de Barcelona y Madrid.",
         pulls=[dict(table=59056, pattern=rf"^{R}\. Total\. Variación anual\.$", regions=CCAA),
                dict(table=59060, pattern=rf"^{R}\. Variación anual\. Total\.$", regions=MUNICIPALITIES)]),
    # ---- INE: population (Estadística Continua de Población, stock at a date)
    dict(id="es-population", source="ine", unit="personas", frequency="quarterly", real="not_applicable", sa=False, point=True,
         name_es="Población residente", name_en="Resident population",
         notes="Estadística Continua de Población; población a la fecha (period_start = period_end). Nacional y CCAA.",
         pulls=[dict(table=79274, pattern=rf"^Total\. {R}\. Total\. Total\. Población\. Número\.$", regions=CCAA)]),
    dict(id="es-population-foreign-nationality", source="ine", unit="personas", frequency="quarterly", real="not_applicable", sa=False, point=True,
         name_es="Población residente de nacionalidad extranjera", name_en="Resident population with foreign nationality",
         notes="Por nacionalidad (los nacionalizados cuentan como españoles). Nacional y CCAA.",
         pulls=[dict(table=79274, pattern=rf"^Total\. {R}\. Extranjera\. Total\. Población\. Número\.$", regions=CCAA)]),
    dict(id="es-population-foreign-born", source="ine", unit="personas", frequency="quarterly", real="not_applicable", sa=False, point=True,
         name_es="Población residente nacida en el extranjero", name_en="Foreign-born resident population",
         notes="Por país de nacimiento, cualquier nacionalidad (incluye españoles nacidos fuera). Nacional y CCAA.",
         pulls=[dict(table=79274, pattern=rf"^Total\. {R}\. Total\. Extranjero\. Población\. Número\.$", regions=CCAA)]),
    # ---- Eurostat (Spain and EU-27 for comparison)
    dict(id="es-gdp-growth-yoy", source="eurostat", unit="%", frequency="quarterly", real="real", sa=True,
         name_es="Crecimiento del PIB real (interanual)", name_en="Real GDP growth (year on year)",
         notes="Volúmenes encadenados; variación sobre el mismo trimestre del año anterior; ajuste estacional y de calendario. España y UE-27.",
         dataset="namq_10_gdp", filters=dict(na_item="B1GQ", unit="CLV_PCH_SM", s_adj="SCA")),
    dict(id="es-gov-debt-pct-gdp", source="eurostat", unit="% PIB", frequency="annual", real="not_applicable", sa=False,
         name_es="Deuda pública (PDE) en % del PIB", name_en="General government gross debt (EDP), % of GDP",
         notes="Administraciones públicas (S13). España y UE-27.",
         dataset="gov_10dd_edpt1", filters=dict(na_item="GD", sector="S13", unit="PC_GDP")),
    dict(id="es-gov-balance-pct-gdp", source="eurostat", unit="% PIB", frequency="annual", real="not_applicable", sa=False,
         name_es="Saldo de las administraciones públicas en % del PIB (déficit negativo)", name_en="General government net lending (+)/borrowing (-), % of GDP",
         notes="Administraciones públicas (S13), PDE. España y UE-27.",
         dataset="gov_10dd_edpt1", filters=dict(na_item="B9", sector="S13", unit="PC_GDP")),
    dict(id="es-tax-revenue-pct-gdp", source="eurostat", unit="% PIB", frequency="annual", real="not_applicable", sa=False,
         name_es="Ingresos por impuestos y cotizaciones sociales en % del PIB", name_en="Total tax revenue incl. social contributions, % of GDP",
         notes="Agregado D2+D5+D91+D61 menos D995 (importes no cobrables), AAPP e instituciones de la UE (S13_S212). España y UE-27.",
         dataset="gov_10a_taxag", filters=dict(na_item="D2_D5_D91_D61_M_D995", sector="S13_S212", unit="PC_GDP")),
    dict(id="es-gini", source="eurostat", unit="índice 0-100", frequency="annual", real="not_applicable", sa=False,
         name_es="Coeficiente de Gini de la renta disponible equivalente", name_en="Gini coefficient of equivalised disposable income",
         notes="EU-SILC; el año es el de la encuesta (la renta se refiere al año anterior). España y UE-27.",
         dataset="ilc_di12", filters=dict(age="TOTAL", statinfo="GINI_HND")),
    dict(id="es-minimum-wage-monthly", source="eurostat", unit="EUR/mes", frequency="other", real="nominal", sa=False,
         name_es="Salario mínimo mensual (Eurostat, prorrateado a 12 pagas)", name_en="Monthly minimum wage (Eurostat, 12-month basis)",
         notes="Datos semestrales (S1 = enero, S2 = julio). Eurostat prorratea a 12 meses los salarios pagados en 14 pagas (caso del SMI).",
         dataset="earn_mw_cur", filters=dict(currency="EUR"), geos={"ES": "es"}),
]
EU_GEOS = {"ES": "es", "EU27_2020": "eu"}


# --------------------------------------------------------------------------------------------- fetching
def http_json(url: str, tries: int = 3):
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "kb-ingest/1.0"})
            raw = urllib.request.urlopen(req, timeout=180, context=SSL_CTX).read()
            for enc in ("utf-8", "latin-1"):
                try:
                    return json.loads(raw.decode(enc))
                except UnicodeDecodeError:
                    continue
        except Exception as e:  # network hiccups, HTTP 5xx
            if attempt == tries - 1:
                raise
            print(f"  retry {url} ({e})", file=sys.stderr)
            time.sleep(3 * (attempt + 1))


def end_of_period(start: dt.date, freq: str, point: bool) -> dt.date:
    if point:
        return start
    if freq == "monthly":
        return start.replace(day=calendar.monthrange(start.year, start.month)[1])
    if freq == "quarterly":
        m = start.month + 2
        return dt.date(start.year, m, calendar.monthrange(start.year, m)[1])
    if freq == "annual":
        return dt.date(start.year, 12, 31)
    return start


def ine_date(obs) -> dt.date | None:
    """Start date of an INE observation: 'Fecha' when present, else year + period code (M01, T1, A...)."""
    fecha = obs.get("Fecha")
    if isinstance(fecha, str):
        return dt.date.fromisoformat(fecha[:10])
    year, period = obs.get("Anyo"), str(obs.get("T3_Periodo") or "")
    if not year:
        return None
    m = re.fullmatch(r"M(\d{2})", period)
    if m:
        return dt.date(int(year), int(m.group(1)), 1)
    m = re.fullmatch(r"T([1-4])", period)
    if m:
        return dt.date(int(year), 3 * int(m.group(1)) - 2, 1)
    if period in ("A", ""):
        return dt.date(int(year), 1, 1)
    return None


_ine_cache: dict[int, list] = {}


def fetch_ine(spec) -> list[tuple]:
    rows = []
    for pull in spec["pulls"]:
        table = pull["table"]
        if table not in _ine_cache:
            print(f"  INE table {table} ...", file=sys.stderr)
            _ine_cache[table] = http_json(INE_TABLE.format(table=table)) or []
        pat = re.compile(pull["pattern"])
        matched = 0
        for series in _ine_cache[table]:
            m = pat.match(series["Nombre"].strip())
            if not m:
                continue
            if "region" in m.groupdict():
                jur = pull["regions"].get(norm(m.group("region")))
                if not jur:
                    continue
            else:
                jur = pull["default_region"]
            matched += 1
            for obs in series.get("Data", []):
                if obs.get("Valor") is None or obs.get("Secreto"):
                    continue
                start = ine_date(obs)
                if start is None:
                    continue
                rows.append((jur, start, end_of_period(start, spec["frequency"], spec.get("point", False)), obs["Valor"]))
        if not matched:
            raise RuntimeError(f"{spec['id']}: no series matched in INE table {table}; series names may have changed")
    return rows


def eurostat_period(label: str):
    if re.fullmatch(r"\d{4}", label):
        y = int(label)
        return dt.date(y, 1, 1), dt.date(y, 12, 31)
    m = re.fullmatch(r"(\d{4})-Q([1-4])", label)
    if m:
        y, q = int(m.group(1)), int(m.group(2))
        s = dt.date(y, 3 * q - 2, 1)
        return s, end_of_period(s, "quarterly", False)
    m = re.fullmatch(r"(\d{4})-S([12])", label)
    if m:
        y, h = int(m.group(1)), int(m.group(2))
        return (dt.date(y, 1, 1), dt.date(y, 6, 30)) if h == 1 else (dt.date(y, 7, 1), dt.date(y, 12, 31))
    m = re.fullmatch(r"(\d{4})-(\d{2})", label)
    if m:
        s = dt.date(int(m.group(1)), int(m.group(2)), 1)
        return s, end_of_period(s, "monthly", False)
    raise ValueError(f"unknown Eurostat period {label!r}")


def fetch_eurostat(spec) -> list[tuple]:
    geos = spec.get("geos", EU_GEOS)
    params = "".join(f"&{k}={v}" for k, v in spec["filters"].items()) + "".join(f"&geo={g}" for g in geos)
    d = http_json(EUROSTAT.format(dataset=spec["dataset"]) + params)
    ids, sizes = d["id"], d["size"]
    for dim, size in zip(ids, sizes):
        if dim not in ("geo", "time") and size != 1:
            raise RuntimeError(f"{spec['id']}: dimension {dim} not fixed by filters ({size} values)")
    strides = [1] * len(ids)
    for i in range(len(ids) - 2, -1, -1):
        strides[i] = strides[i + 1] * sizes[i + 1]
    gi, ti = ids.index("geo"), ids.index("time")
    geo_idx = d["dimension"]["geo"]["category"]["index"]
    time_idx = d["dimension"]["time"]["category"]["index"]
    rows = []
    for geo, g in geo_idx.items():
        for label, t in time_idx.items():
            v = d["value"].get(str(g * strides[gi] + t * strides[ti]))
            if v is None:
                continue
            start, end = eurostat_period(label)
            rows.append((geos[geo], start, end, v))
    return rows


# --------------------------------------------------------------------------------------------- writing
def num(v) -> str:
    f = float(v)
    return str(int(f)) if f.is_integer() and abs(f) < 1e15 else repr(f)


def write_series(spec, rows, retrieved: str):
    path = DATA / "indicators" / f"{spec['id']}.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = sorted(set(rows), key=lambda r: (r[0], r[1]))
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["indicator_id", "jurisdiction_id", "period_start", "period_end", "value", "retrieved"])
        for jur, start, end, value in rows:
            w.writerow([spec["id"], jur, start.isoformat(), end.isoformat(), num(value), retrieved])
    return path, rows


def upsert_csv(path: Path, key: str, new_rows: list[dict]):
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        header, existing = reader.fieldnames, list(reader)
    by_key = {r[key]: r for r in existing}
    for r in new_rows:
        by_key[r[key]] = {h: r.get(h, "") for h in header}
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=header, lineterminator="\n")
        w.writeheader()
        for k in sorted(by_key):
            w.writerow(by_key[k])


def definition(spec) -> dict:
    if spec["source"] == "ine":
        code = "INE tabla " + ", ".join(str(p["table"]) for p in spec["pulls"])
    else:
        code = "Eurostat " + spec["dataset"] + " (" + ", ".join(f"{k}={v}" for k, v in spec["filters"].items()) + ")"
    return dict(indicator_id=spec["id"], name_es=spec["name_es"], name_en=spec["name_en"], unit=spec["unit"],
                frequency=spec["frequency"], source_id=spec["source"], series_code=code,
                real_or_nominal=spec["real"], seasonally_adjusted="true" if spec["sa"] else "false", notes=spec["notes"])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", nargs="+", help="indicator ids to ingest")
    ap.add_argument("--list", action="store_true", help="list available indicators")
    args = ap.parse_args()
    if args.list:
        for s in SPECS:
            print(f"{s['id']:40} {s['source']:9} {s['frequency']:10} {s['name_es']}")
        return
    specs = [s for s in SPECS if not args.only or s["id"] in args.only]
    if args.only and len(specs) != len(args.only):
        sys.exit(f"unknown ids: {set(args.only) - {s['id'] for s in SPECS}}")
    retrieved = dt.date.today().isoformat()
    done, failed = [], []
    for spec in specs:
        try:
            rows = fetch_ine(spec) if spec["source"] == "ine" else fetch_eurostat(spec)
            path, rows = write_series(spec, rows, retrieved)
            jurs = sorted({r[0] for r in rows})
            print(f"{spec['id']}: {len(rows)} obs, {rows[0][1]} → {rows[-1][1] if rows else ''}, {len(jurs)} jurisdictions")
            done.append(spec)
        except Exception as e:
            print(f"FAILED {spec['id']}: {e}", file=sys.stderr)
            failed.append(spec["id"])
    if done:
        upsert_csv(DATA / "indicator_defs.csv", "indicator_id", [definition(s) for s in done])
        all_ids = sorted({p.stem for p in (DATA / "indicators").glob("*.csv")})
        upsert_csv(DATA / "coverage.csv", "coverage_id", [dict(
            coverage_id="es-cov-indicators", jurisdiction_id="es", dataset="indicators", completeness="partial",
            method="ingestion", last_checked=retrieved,
            notes="Series automáticas (tools/ingest_indicators.py): " + ", ".join(all_ids))])
    if failed:
        sys.exit(f"failed: {failed}")


if __name__ == "__main__":
    main()

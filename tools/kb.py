#!/usr/bin/env python3
"""kb.py - build, validate and query the politics knowledge base.

Run through the wrappers in the repo root: `./kb <command>` (bash) or `.\\kb.cmd <command>` (PowerShell / cmd).

Commands
  build                         validate sources and (re)build build/kb.duckdb + SCHEMA.md
  validate                      validate only (exit code 1 if there are errors)
  sql "<SQL>" | sql -           read-only DuckDB query (auto-rebuilds when sources changed); '-' reads SQL from stdin
  search "<text>" [--type T]    full-text search (BM25, stemmed, accent-insensitive) over titles, summaries, bodies
  context <YYYY-MM-DD> [--jurisdiction es-ct]   governments, legislature, seats, indicators, events at a date
  schema [TABLE ...]            compact description of tables and columns
  new <type> <id> [--dir SUB]   create a Markdown entity skeleton from the schema
  add <table> --json '<obj|list>' [--file PATH]   append row(s) to a CSV table; topics/actors/citations/related
                                go to the link tables automatically
  stale                         questions whose evidence changed after the answer was written
  scaffold [--country es]       create missing CSV files (header only)

Sources of truth: schema/tables.yaml, data/**/*.csv and Markdown under entries/, library/, knowledge/, questions/.
build/kb.duckdb is derived and can always be deleted.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import re
import sys
import unicodedata
from pathlib import Path

try:
    import duckdb
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("Missing dependencies. From the repo root run:\n"
             "  python -m venv .venv && .venv/Scripts/python -m pip install -r requirements.txt   (Windows)\n"
             "  python3 -m venv .venv && .venv/bin/python -m pip install -r requirements.txt     (Linux/macOS)")

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_FILE = ROOT / "schema" / "tables.yaml"
VIEWS_FILE = ROOT / "schema" / "views.sql"
SCHEMA_MD = ROOT / "SCHEMA.md"
DB_FILE = ROOT / "build" / "kb.duckdb"
MD_ROOTS = ("entries", "library", "knowledge", "questions")
SOURCE_DIRS = ("schema", "data") + MD_ROOTS
SOURCE_EXT = (".csv", ".md", ".yaml", ".sql")
TYPE_SQL = {"id": "VARCHAR", "text": "VARCHAR", "url": "VARCHAR", "enum": "VARCHAR",
            "int": "BIGINT", "float": "DOUBLE", "bool": "BOOLEAN", "date": "DATE"}
STEMMERS = {"es": "spanish", "en": "english", "ca": "catalan", "eu": "basque", "gl": "galician",
            "fr": "french", "de": "german", "it": "italian", "pt": "portuguese"}
COUNTRY_LANG = {"es": "es"}  # default language of a country's content (CSV titles, new entries)
MAX_ERRORS_PER_CHECK = 20

if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8")
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")


# ----------------------------------------------------------------------------- helpers
def q(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def lit(value) -> str:
    return "'" + str(value).replace("'", "''") + "'"


def rel(path) -> str:
    return Path(path).resolve().relative_to(ROOT).as_posix()


def today() -> str:
    return dt.date.today().isoformat()


def to_str(value):
    """Normalise a YAML/JSON scalar to the string stored in raw tables (None for empty)."""
    if value is None:
        return None
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (dt.date, dt.datetime)):
        return value.isoformat()[:10]
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False)
    s = str(value).strip()
    return s or None


def fail(msg: str, code: int = 2):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def read_header(path: Path) -> list[str]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return [h.strip() for h in next(csv.reader(f), [])]


class _FrontMatterLoader(yaml.SafeLoader):
    """SafeLoader that keeps dates as strings, so bad dates become validation errors instead of parse failures."""


_FrontMatterLoader.yaml_implicit_resolvers = {
    k: [(tag, rx) for tag, rx in v if tag != "tag:yaml.org,2002:timestamp"]
    for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()}

FM_RE = re.compile(r"\A---[ \t]*\n(.*?)\n---[ \t]*(?:\n|\Z)(.*)\Z", re.S)


def read_md(path: Path):
    text = path.read_text(encoding="utf-8-sig")
    m = FM_RE.match(text)
    if not m:
        raise ValueError("missing YAML front matter (file must start with ---)")
    meta = yaml.load(m.group(1), Loader=_FrontMatterLoader) or {}
    if not isinstance(meta, dict):
        raise ValueError("front matter is not a mapping")
    return meta, m.group(2)


def known_countries() -> set[str]:
    path = ROOT / "data" / "common" / "jurisdictions.csv"
    out = set()
    if path.exists():
        with path.open(encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                if row.get("level") == "state":
                    out.add(row["jurisdiction_id"])
    return out


def country_of(id_: str, countries: set[str]) -> str:
    m = re.match(r"^([a-z]{2})-", id_ or "")
    return m.group(1) if m and m.group(1) in countries else "global"


# ----------------------------------------------------------------------------- schema
class Schema:
    def __init__(self):
        raw = yaml.safe_load(SCHEMA_FILE.read_text(encoding="utf-8"))
        self.common = raw["md_common"]
        self.tables: dict = raw["tables"]
        self.md_by_type = {}
        for name, t in self.tables.items():
            t["name"] = name
            if t["kind"] == "md":
                self.md_by_type[t["entity_type"]] = name
        self.common["columns"]["type"]["values"] = sorted(self.md_by_type)
        for t in self.tables.values():
            if t["kind"] == "md":
                required = set(t.get("required_common") or [])
                cols = {}
                for c, spec in self.common["columns"].items():
                    spec = dict(spec)
                    if c in required:
                        spec["required"] = True
                    cols[c] = spec
                cols.update(t.get("columns") or {})
                t["all_columns"] = cols
                t["all_lists"] = {**self.common["lists"], **(t.get("lists") or {})}
            else:
                t["all_columns"] = t.get("columns") or {}
                t["all_lists"] = {}
        self._check()

    def _check(self):
        for name, t in self.tables.items():
            for c, spec in t["all_columns"].items():
                if spec.get("type") not in TYPE_SQL:
                    fail(f"schema: {name}.{c} has unknown type {spec.get('type')!r}")
                fk = spec.get("fk")
                if fk and fk != "*" and fk not in self.tables:
                    fail(f"schema: {name}.{c} references unknown table {fk!r}")
            for lf, ls in t["all_lists"].items():
                if ls["table"] not in self.tables:
                    fail(f"schema: list {name}.{lf} targets unknown table {ls['table']!r}")
            for k in t.get("key", []):
                if k not in t["all_columns"]:
                    fail(f"schema: key column {name}.{k} not defined")

    def of_kind(self, *kinds):
        return [t for t in self.tables.values() if t["kind"] in kinds]

    def entity_tables(self):
        return [t for t in self.tables.values() if t["kind"] == "md" or t.get("entity")]


# ----------------------------------------------------------------------------- loading
def create_raw(con, t):
    cols = ", ".join(f"{q(c)} VARCHAR" for c in list(t["all_columns"]) + ["_src"])
    con.execute(f"CREATE TABLE {q('raw_' + t['name'])} ({cols})")


def csv_files(t) -> list[Path]:
    pattern = re.sub(r"\{[^}]+\}", "*", t["path"])
    return sorted(ROOT.glob(pattern))


def load_csv_table(con, t, errors):
    cols = list(t["all_columns"])
    prefix = ROOT.as_posix() + "/"
    for f in csv_files(t):
        hdr = read_header(f)
        if not hdr:
            continue
        unknown = [h for h in hdr if h not in cols]
        missing = [c for c in cols if c not in hdr]
        if unknown or missing:
            errors.append(f"{rel(f)}: header differs from schema (missing {missing}, unknown {unknown})")
        sel = ", ".join(f"NULLIF(trim({q(c)}), '')" if c in hdr else "NULL" for c in cols)
        try:
            con.execute(
                f"INSERT INTO {q('raw_' + t['name'])} SELECT {sel}, replace(filename, {lit(prefix)}, '') "
                f"FROM read_csv({lit(f.as_posix())}, header=true, all_varchar=true, filename=true, "
                f"delim=',', quote='\"', escape='\"')")
        except duckdb.Error as e:
            errors.append(f"{rel(f)}: cannot parse CSV: {str(e).splitlines()[0]}")


def scan_markdown(schema: Schema, countries, errors):
    rows = {t["name"]: [] for t in schema.of_kind("md", "link", "child")}
    docs = []
    for root in MD_ROOTS:
        base = ROOT / root
        if not base.exists():
            continue
        for path in sorted(base.rglob("*.md")):
            if path.name.lower() == "readme.md":
                continue
            src = rel(path)
            try:
                meta, body = read_md(path)
            except Exception as e:  # yaml errors, encoding...
                errors.append(f"{src}: {e}")
                continue
            typ = meta.get("type")
            tname = schema.md_by_type.get(typ)
            if not tname:
                errors.append(f"{src}: unknown or missing type {typ!r} (valid: {sorted(schema.md_by_type)})")
                continue
            t = schema.tables[tname]
            id_ = to_str(meta.get("id")) or ""
            if id_ != path.stem:
                errors.append(f"{src}: id {id_!r} must equal the file name {path.stem!r}")
            folder = t["folder"].replace("{country}", country_of(id_, countries))
            parent = path.parent.relative_to(ROOT).as_posix()
            if not (parent == folder or (t.get("free_subfolders") and parent.startswith(folder + "/"))):
                errors.append(f"{src}: a '{typ}' must live in {folder}/")
            row = {"_src": src}
            for key, value in meta.items():
                if key in t["all_columns"]:
                    if isinstance(value, (list, dict)):
                        errors.append(f"{src}: field '{key}' must be a single value")
                        continue
                    row[key] = to_str(value)
                elif key not in t["all_lists"]:
                    errors.append(f"{src}: unknown field '{key}'")
            rows[tname].append(row)
            for lf, ls in t["all_lists"].items():
                items = meta.get(lf)
                if items is None:
                    continue
                if not isinstance(items, list):
                    errors.append(f"{src}: '{lf}' must be a list")
                    continue
                target = schema.tables[ls["table"]]
                for item in items:
                    r = {"entity_id": id_, "_src": src}
                    r.update({k: to_str(v) for k, v in (ls.get("defaults") or {}).items()})
                    if isinstance(item, dict):
                        bad = [k for k in item if k not in target["all_columns"] or k == "entity_id"]
                        if bad:
                            errors.append(f"{src}: '{lf}' item has unknown keys {bad}")
                            continue
                        r.update({k: to_str(v) for k, v in item.items()})
                    elif "scalar_column" in ls:
                        r[ls["scalar_column"]] = to_str(item)
                    else:
                        errors.append(f"{src}: '{lf}' items must be mappings with keys {list(target['all_columns'])}")
                        continue
                    rows[ls["table"]].append(r)
            docs.append((id_, typ, to_str(meta.get("lang")), to_str(meta.get("title")),
                         to_str(meta.get("summary")), body.strip(), src))
    return rows, docs


def insert_rows(con, t, rows):
    if not rows:
        return
    cols = list(t["all_columns"]) + ["_src"]
    con.executemany(
        f"INSERT INTO {q('raw_' + t['name'])} ({', '.join(q(c) for c in cols)}) VALUES ({', '.join('?' * len(cols))})",
        [[r.get(c) for c in cols] for r in rows])


# ----------------------------------------------------------------------------- validation
def validate_raw(con, schema: Schema, errors):
    # global registry of entity ids
    parts = []
    for t in schema.entity_tables():
        k = t["key"][0]
        parts.append(f"SELECT {q(k)} AS id, {lit(t['name'])} AS tbl FROM {q('raw_' + t['name'])}")
    con.execute("CREATE TEMP TABLE _entity_ids AS " + " UNION ALL ".join(parts))
    for row in con.execute("SELECT id, string_agg(tbl, ', ') FROM _entity_ids WHERE id IS NOT NULL "
                           "GROUP BY id HAVING count(*) > 1 LIMIT 50").fetchall():
        errors.append(f"duplicate entity id {row[0]!r} in: {row[1]}")

    for t in schema.tables.values():
        raw = q("raw_" + t["name"])
        keycols = t["key"]
        keyexpr = " || '|' || ".join(f"coalesce({q(k)}, '-')" for k in keycols)
        checks = []  # (message, condition, value expression)
        for c, spec in t["all_columns"].items():
            qc, typ = q(c), spec["type"]
            if spec.get("required"):
                checks.append((f"missing required '{c}'", f"{qc} IS NULL", "NULL"))
            if typ == "date":
                checks.append((f"'{c}' must be a date YYYY-MM-DD",
                               f"{qc} IS NOT NULL AND (NOT regexp_matches({qc}, '^[0-9]{{4}}-[0-9]{{2}}-[0-9]{{2}}$') "
                               f"OR TRY_CAST({qc} AS DATE) IS NULL)", qc))
            elif typ in ("int", "float", "bool"):
                checks.append((f"'{c}' must be {typ}", f"{qc} IS NOT NULL AND TRY_CAST({qc} AS {TYPE_SQL[typ]}) IS NULL", qc))
            elif typ == "url":
                checks.append((f"'{c}' must be an http(s) URL", f"{qc} IS NOT NULL AND NOT regexp_matches({qc}, '^https?://')", qc))
            if typ == "enum" and spec.get("values"):
                values = ", ".join(lit(v) for v in spec["values"])
                checks.append((f"'{c}' not in [{'|'.join(map(str, spec['values']))}]",
                               f"{qc} IS NOT NULL AND {qc} NOT IN ({values})", qc))
            if spec.get("max_len"):
                checks.append((f"'{c}' longer than {spec['max_len']} chars",
                               f"length({qc}) > {int(spec['max_len'])}", f"length({qc})"))
        if t.get("id_pattern"):
            k = q(keycols[0])
            checks.append((f"id does not match {t['id_pattern']}",
                           f"{k} IS NOT NULL AND NOT regexp_matches({k}, {lit(t['id_pattern'])})", k))
        for msg, cond, valexpr in checks:
            for key, src, val in con.execute(
                    f"SELECT {keyexpr}, _src, CAST({valexpr} AS VARCHAR) FROM {raw} WHERE {cond} "
                    f"LIMIT {MAX_ERRORS_PER_CHECK}").fetchall():
                shown = f" (got {val!r})" if val is not None and valexpr != "NULL" else ""
                errors.append(f"{t['name']}[{key}] {src}: {msg}{shown}")
        # primary key uniqueness
        cols = ", ".join(q(k) for k in keycols)
        for key, n, srcs in con.execute(
                f"SELECT {keyexpr}, count(*), string_agg(DISTINCT _src, ', ') FROM {raw} "
                f"GROUP BY {cols} HAVING count(*) > 1 LIMIT {MAX_ERRORS_PER_CHECK}").fetchall():
            errors.append(f"{t['name']}[{key}]: duplicate key ({n} rows) in {srcs}")
        # foreign keys
        rkeyexpr = " || '|' || ".join(f"coalesce(r.{q(k)}, '-')" for k in keycols)
        for c, spec in t["all_columns"].items():
            fk = spec.get("fk")
            if not fk:
                continue
            if fk == "*":
                target, tkey = "_entity_ids", "id"
            else:
                target, tkey = q("raw_" + fk), q(schema.tables[fk]["key"][0])
            for key, src, val in con.execute(
                    f"SELECT {rkeyexpr}, r._src, r.{q(c)} FROM {raw} r LEFT JOIN {target} x ON r.{q(c)} = x.{tkey} "
                    f"WHERE r.{q(c)} IS NOT NULL AND x.{tkey} IS NULL LIMIT {MAX_ERRORS_PER_CHECK}").fetchall():
                errors.append(f"{t['name']}[{key}] {src}: '{c}' = {val!r} not found in {fk if fk != '*' else 'any entity'}")


# ----------------------------------------------------------------------------- build
def create_typed(con, t):
    sels = []
    for c, spec in t["all_columns"].items():
        if spec["type"] in ("int", "float", "bool", "date"):
            sels.append(f"TRY_CAST({q(c)} AS {TYPE_SQL[spec['type']]}) AS {q(c)}")
        else:
            sels.append(q(c))
    if t["kind"] == "md":
        sels.append("_src AS path")
    con.execute(f"CREATE TABLE {q(t['name'])} AS SELECT {', '.join(sels)} FROM {q('raw_' + t['name'])}")


def create_entities_view(con, schema: Schema):
    parts = []
    for t in schema.entity_tables():
        if t["kind"] == "md":
            parts.append(f"SELECT id, type, title, summary, date, jurisdiction_id, path, updated FROM {q(t['name'])}")
        else:
            e, k = t["entity"], t["key"][0]
            summary = "summary" if "summary" in t["all_columns"] else "NULL"
            parts.append(f"SELECT {q(k)} AS id, {lit(e['type'])} AS type, CAST({e['title']} AS VARCHAR) AS title, "
                         f"CAST({summary} AS VARCHAR) AS summary, CAST({q(e['date'])} AS DATE) AS date, jurisdiction_id, "
                         f"CAST(NULL AS VARCHAR) AS path, CAST(NULL AS DATE) AS updated FROM {q(t['name'])}")
    con.execute("CREATE VIEW entities AS " + " UNION ALL ".join(parts))


def load_fts(con, install=False) -> bool:
    try:
        con.execute("LOAD fts")
        return True
    except duckdb.Error:
        if not install:
            return False
    try:
        con.execute("INSTALL fts")
        con.execute("LOAD fts")
        return True
    except duckdb.Error:
        return False


def build_documents(con, schema: Schema, docs, warnings):
    con.execute("CREATE TABLE documents (id VARCHAR, type VARCHAR, lang VARCHAR, title VARCHAR, summary VARCHAR, "
                "body VARCHAR, path VARCHAR, norm VARCHAR)")
    if docs:
        con.executemany("INSERT INTO documents (id, type, lang, title, summary, body, path) VALUES (?, ?, ?, ?, ?, ?, ?)", docs)
    lang_case = "CASE split_part(id, '-', 1) " + " ".join(
        f"WHEN {lit(c)} THEN {lit(l)}" for c, l in COUNTRY_LANG.items()) + " ELSE 'en' END"
    for t in schema.entity_tables():
        if t["kind"] != "md" and "title" in t["all_columns"]:
            summary = "summary" if "summary" in t["all_columns"] else "NULL"
            con.execute(f"INSERT INTO documents (id, type, lang, title, summary) "
                        f"SELECT id, type, {lang_case}, title, {summary} FROM "
                        f"(SELECT {q(t['key'][0])} AS id, {lit(t['entity']['type'])} AS type, title, "
                        f"{summary if summary == 'NULL' else 'summary'} AS summary FROM {q(t['name'])})")
    if not load_fts(con, install=True):
        warnings.append("DuckDB 'fts' extension unavailable: search falls back to substring matching")
        return
    stemmers = {}
    for lang, stemmer in STEMMERS.items():
        try:
            con.execute("SELECT stem('prueba', ?)", [stemmer])
            stemmers[lang] = stemmer
        except duckdb.Error:
            pass
    case = "CASE lang " + " ".join(f"WHEN {lit(k)} THEN {lit(v)}" for k, v in stemmers.items()) + " ELSE 'none' END"
    con.execute(f"CREATE MACRO kb_stemmer(lang) AS {case}")
    con.execute(r"""CREATE MACRO kb_norm(txt, stemmer) AS array_to_string(
        list_transform(
            list_filter(regexp_split_to_array(lower(coalesce(txt, '')), '[^\p{L}\p{N}]+'), lambda w: length(w) > 1),
            lambda w: strip_accents(stem(stem(w, stemmer), stemmer))),
        ' ')""")
    con.execute("UPDATE documents SET norm = kb_norm(concat_ws(' ', title, title, summary, body), kb_stemmer(lang))")
    con.execute("PRAGMA create_fts_index('documents', 'id', 'norm', stemmer='none', stopwords='none', "
                "ignore='[^a-z0-9]+', strip_accents=0, lower=1, overwrite=1)")


def build(write: bool = True, quiet: bool = False) -> int:
    schema = Schema()
    countries = known_countries()
    errors: list[str] = []
    warnings: list[str] = []
    if write:
        DB_FILE.parent.mkdir(parents=True, exist_ok=True)
        tmp = DB_FILE.with_name(f"kb.tmp{os.getpid()}.duckdb")
        now = dt.datetime.now().timestamp()
        for p in DB_FILE.parent.glob("kb.tmp*"):  # leftovers of crashed builds
            if p.name.startswith(tmp.name) or now - p.stat().st_mtime > 600:
                p.unlink(missing_ok=True)
        con = duckdb.connect(str(tmp))
    else:
        con = duckdb.connect()
    ok = False
    try:
        for t in schema.tables.values():
            create_raw(con, t)
        for t in schema.of_kind("csv", "link"):
            load_csv_table(con, t, errors)
        md_rows, docs = scan_markdown(schema, countries, errors)
        for name, rows in md_rows.items():
            insert_rows(con, schema.tables[name], rows)
        validate_raw(con, schema, errors)
        if write:
            for t in schema.tables.values():
                create_typed(con, t)
            for t in schema.tables.values():
                con.execute(f"DROP TABLE {q('raw_' + t['name'])}")
            create_entities_view(con, schema)
            con.execute(VIEWS_FILE.read_text(encoding="utf-8"))
            build_documents(con, schema, docs, warnings)
            counts = con.execute("SELECT (SELECT count(*) FROM entities), (SELECT count(*) FROM documents)").fetchone()
        ok = True
    finally:
        con.close()
        if write and not ok:
            for p in DB_FILE.parent.glob(tmp.name + "*"):
                p.unlink(missing_ok=True)
    if write:
        try:
            os.replace(tmp, DB_FILE)
        except OSError as e:
            fail(f"could not replace {rel(DB_FILE)} (is it open in another process?): {e}")
        write_schema_md(schema)
    out = sys.stderr if quiet else sys.stdout
    shown = errors if not quiet else errors[:10]
    for w in warnings:
        print(f"warning: {w}", file=out)
    for e in shown:
        print(f"error: {e}", file=out)
    if len(shown) < len(errors):
        print(f"... {len(errors) - len(shown)} more errors (run: kb validate)", file=out)
    status = f"{len(errors)} errors" if errors else "valid"
    if write:
        print(f"[kb] built {rel(DB_FILE)}: {counts[0]} entities, {counts[1]} documents; {status}", file=out)
    else:
        print(f"[kb] {status}", file=out)
    return 1 if errors else 0


# ----------------------------------------------------------------------------- SCHEMA.md
def col_line(c, spec) -> str:
    s = f"- `{c}` {spec['type']}{'*' if spec.get('required') else ''}"
    if spec.get("fk"):
        s += f" → {spec['fk']}"
    if spec.get("values"):
        s += " [" + "|".join(map(str, spec["values"])) + "]"
    if spec.get("max_len"):
        s += f" (≤{spec['max_len']} chars)"
    if spec.get("desc"):
        s += f" — {spec['desc']}"
    return s


def list_hint(schema: Schema, ls) -> str:
    target = schema.tables[ls["table"]]
    keys = [c for c in target["all_columns"] if c != "entity_id"]
    if "scalar_column" in ls:
        return f"→ {ls['table']}: list of {ls['scalar_column']} values, or mappings with keys {keys}"
    return f"→ {ls['table']}: list of mappings with keys {keys}"


def table_text(schema: Schema, t) -> str:
    where = {"csv": t.get("path"), "link": f"md list fields + optional {t.get('path')}",
             "child": "md list fields", "md": f"{t.get('folder')}/<id>.md"}[t["kind"]]
    lines = [f"### `{t['name']}` ({t['kind']}: {where})", t.get("desc", ""),
             f"key: ({', '.join(t['key'])})" + (f" · id pattern `{t['id_pattern']}`" if t.get("id_pattern") else "")]
    if t["kind"] == "md":
        lines.append(f"front matter `type: {t['entity_type']}` · + common md columns · required: "
                     f"{', '.join(t.get('required_common') or []) or '(only always-required)'}")
        cols = t.get("columns") or {}
    else:
        cols = t["all_columns"]
    lines += [col_line(c, s) for c, s in cols.items()]
    for lf, ls in (t.get("lists") or {}).items():
        lines.append(f"- list `{lf}` {list_hint(schema, ls)}")
    return "\n".join(lines)


def views_doc() -> list[str]:
    out = []
    for line in VIEWS_FILE.read_text(encoding="utf-8").splitlines():
        m = re.match(r"--\s*view:\s*(\S+)\s*—\s*(.*)", line)
        if m:
            out.append(f"- `{m.group(1)}` — {m.group(2)}")
    return out


EXAMPLES = """\
```sql
-- Who governed Spain and Catalonia on a date (shortcut: kb context 2023-05-24 --jurisdiction es-ct)
SELECT jurisdiction_id, head_name, governing_parties, support_parties FROM v_governments
WHERE jurisdiction_id IN ('es', 'es-ct') AND DATE '2023-05-24' BETWEEN valid_from AND coalesce(valid_to, DATE '9999-12-31');

-- How each party voted on housing votes, with the state government at the time
SELECT vp.date, vp.title, vp.object, vp.bundled, vp.party_id, vp.position, c.state_governing_parties
FROM v_vote_party vp
JOIN v_topic_entities te ON te.id = vp.vote_id AND te.root_topic = 'housing'
JOIN v_entity_context c ON c.id = vp.vote_id
ORDER BY vp.date LIMIT 50;

-- Everything a party did on a topic
SELECT a.date, a.entity_type, a.title, a.role_or_position FROM v_party_actions a
JOIN v_topic_entities te ON te.id = a.entity_id AND te.root_topic = 'immigration'
WHERE a.party_id = 'es-vox' ORDER BY a.date;

-- Promise tracking
SELECT party_id, status, count(*) FROM v_promises GROUP BY ALL ORDER BY ALL;

-- Evidence behind knowledge claims on a topic
SELECT claim_id, statement, strength, consensus, n_supporting, n_contradicting, best_grade
FROM v_claims WHERE note_id IN (SELECT id FROM v_topic_entities WHERE root_topic = 'rent_regulation');

-- A statistical series
SELECT period_start, value, unit FROM v_indicators
WHERE indicator_id = 'es-unemployment-rate' AND jurisdiction_id = 'es' ORDER BY period_start;

-- Before concluding that something did not happen: is the dataset complete for that period?
SELECT dataset, topic_id, period_from, period_to, completeness, notes FROM coverage WHERE jurisdiction_id = 'es';
```"""


def schema_text(schema: Schema, names=None) -> str:
    if names:
        missing = [n for n in names if n not in schema.tables]
        if missing:
            fail(f"unknown table(s) {missing}; tables: {sorted(schema.tables)}")
        return "\n\n".join(table_text(schema, schema.tables[n]) for n in names)
    common = schema.common
    parts = [
        "# SCHEMA",
        "_Generated by `kb build` from `schema/tables.yaml` and `schema/views.sql`. Do not edit by hand._",
        "",
        "Query with `kb sql \"<SQL>\"` (DuckDB SQL). Legend: `*` required · `→ t` foreign key to table t "
        "(`→ *` = any entity id) · `[a|b]` allowed values.",
        "Markdown entities: one file per row, file name = id, YAML front matter = the row, list fields → link/child "
        "tables, body → `documents` (full-text search with `kb search`).",
        "",
        "## Common columns of every Markdown entity",
        common.get("desc", ""),
        *[col_line(c, s) for c, s in common["columns"].items()],
        *[f"- list `{lf}` {list_hint(schema, ls)}" for lf, ls in common["lists"].items()],
        "",
        "## Tables",
    ]
    order = ("csv", "md", "link", "child")
    for kind in order:
        for t in schema.of_kind(kind):
            parts += ["", table_text(schema, t)]
    parts += [
        "", "## Built objects",
        "- `entities` (view) — id, type, title, summary, date, jurisdiction_id, path, updated: every entity of every table.",
        "- `documents` (table) — id, type, lang, title, summary, body, path: the searchable text (`kb search`).",
        "", "## Views", *views_doc(),
        "", "## Example queries", EXAMPLES, "",
    ]
    return "\n".join(parts)


def write_schema_md(schema: Schema):
    text = schema_text(schema)
    if not SCHEMA_MD.exists() or SCHEMA_MD.read_text(encoding="utf-8") != text:
        SCHEMA_MD.write_text(text, encoding="utf-8", newline="\n")


# ----------------------------------------------------------------------------- querying
def latest_source_mtime() -> float:
    newest = Path(__file__).stat().st_mtime
    for d in SOURCE_DIRS:
        base = ROOT / d
        if not base.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [x for x in dirnames if not x.startswith(".")]
            newest = max(newest, os.stat(dirpath).st_mtime)
            for fn in filenames:
                if fn.endswith(SOURCE_EXT):
                    newest = max(newest, os.stat(os.path.join(dirpath, fn)).st_mtime)
    return newest


def connect_ro():
    if not DB_FILE.exists() or DB_FILE.stat().st_mtime < latest_source_mtime():
        print("[kb] sources changed, rebuilding...", file=sys.stderr)
        build(write=True, quiet=True)
    con = duckdb.connect(str(DB_FILE), read_only=True)
    load_fts(con)
    return con


def fmt_cell(v, maxw):
    if v is None:
        return ""
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, float) and v.is_integer() and abs(v) < 1e15:
        s = str(v)
    else:
        s = str(v)
    s = s.replace("\r", " ").replace("\n", " ")
    return s if maxw <= 0 or len(s) <= maxw else s[:maxw] + "…"


def print_rows(cols, rows, fmt="csv", maxw=300):
    if fmt == "json":
        print(json.dumps([dict(zip(cols, r)) for r in rows], ensure_ascii=False, default=str))
        return
    cells = [[fmt_cell(v, maxw) for v in r] for r in rows]
    if fmt == "md":
        print("| " + " | ".join(cols) + " |")
        print("|" + "---|" * len(cols))
        for r in cells:
            print("| " + " | ".join(c.replace("|", "\\|") for c in r) + " |")
        return
    w = csv.writer(sys.stdout, lineterminator="\n")
    w.writerow(cols)
    w.writerows(cells)


def run_query(con, sql, params=None, limit=100, fmt="csv", maxw=300):
    cur = con.execute(sql, params or [])
    if cur.description is None:
        print("OK")
        return
    cols = [d[0] for d in cur.description]
    rows = cur.fetchmany(limit + 1)
    truncated = len(rows) > limit
    print_rows(cols, rows[:limit], fmt, maxw)
    if truncated:
        print(f"# truncated at {limit} rows: aggregate, filter, add LIMIT or pass --limit")


def cmd_sql(args):
    sql = sys.stdin.read() if args.query == "-" else args.query
    con = connect_ro()
    try:
        run_query(con, sql, limit=args.limit, fmt=args.format, maxw=0 if args.full else args.width)
    except duckdb.Error as e:
        fail(str(e).strip(), 1)


def fold(s: str) -> str:
    out = []
    for ch in s.lower():
        base = "".join(c for c in unicodedata.normalize("NFKD", ch) if not unicodedata.combining(c))
        out.append(base[:1] if base else ch)
    return "".join(out)


def snippet(texts, query, width=180):
    """Fragment around the first query word found in the first text that contains one; else start of the first text."""
    texts = [t for t in texts if t]
    if not texts:
        return ""
    tokens = [fold(w)[:5] for w in re.findall(r"\w+", query) if len(w) > 2]
    for text in texts:
        folded = fold(text)
        pos = min((p for p in (folded.find(tok) for tok in tokens) if p >= 0), default=-1)
        if pos >= 0:
            start = max(0, pos - width // 3)
            frag = re.sub(r"\s+", " ", text[start:start + width])
            return ("…" if start else "") + frag + ("…" if start + width < len(text) else "")
    text = texts[0]
    return re.sub(r"\s+", " ", text[:width]) + ("…" if len(text) > width else "")


def cmd_search(args):
    con = connect_ro()
    has_index = con.execute("SELECT count(*) FROM duckdb_schemas() WHERE schema_name = 'fts_main_documents'").fetchone()[0]
    fts = has_index and load_fts(con)
    langs = [args.lang] if args.lang else [r[0] for r in con.execute(
        "SELECT DISTINCT lang FROM documents WHERE lang IS NOT NULL").fetchall()]
    type_filter = " AND type = ?" if args.type else ""
    hits = []
    if fts:
        for lang in langs:
            qn = con.execute("SELECT kb_norm(?, kb_stemmer(?))", [args.query, lang]).fetchone()[0]
            if not qn:
                continue
            params = [qn, lang] + ([args.type] if args.type else []) + [args.limit]
            hits += con.execute(
                "SELECT id, type, title, path, [summary, body, title], score FROM ("
                "SELECT *, fts_main_documents.match_bm25(id, ?) AS score FROM documents WHERE lang = ?" + type_filter +
                ") WHERE score IS NOT NULL ORDER BY score DESC LIMIT ?", params).fetchall()
    else:
        words = [w for w in re.findall(r"\w+", args.query) if len(w) > 2] or [args.query]
        score = " + ".join("(strip_accents(lower(concat_ws(' ', title, summary, body))) LIKE '%' || strip_accents(lower(?)) || '%')::INT"
                           for _ in words)
        hits = con.execute(
            f"SELECT id, type, title, path, [summary, body, title], {score} AS score FROM documents "
            f"WHERE {score} > 0" + type_filter + " ORDER BY score DESC LIMIT ?",
            words + words + ([args.type] if args.type else []) + [args.limit]).fetchall()
    hits.sort(key=lambda h: -h[5])
    rows = [(round(h[5], 3), h[0], h[1], h[2], h[3], snippet(h[4], args.query)) for h in hits[:args.limit]]
    print_rows(["score", "id", "type", "title", "path", "snippet"], rows, args.format, 0)
    if not rows:
        print("# no matches (try other words, the other language, or kb sql on entities/topics)")


def cmd_context(args):
    try:
        day = dt.date.fromisoformat(args.date)
    except ValueError:
        fail("date must be YYYY-MM-DD")
    con = connect_ro()
    chain = [r[0] for r in con.execute(
        "WITH RECURSIVE up(id, parent, depth) AS ("
        " SELECT jurisdiction_id, parent_id, 0 FROM jurisdictions WHERE jurisdiction_id = ?"
        " UNION ALL SELECT j.jurisdiction_id, j.parent_id, up.depth + 1 FROM jurisdictions j JOIN up ON j.jurisdiction_id = up.parent)"
        " SELECT id FROM up ORDER BY depth", [args.jurisdiction]).fetchall()]
    if not chain:
        fail(f"unknown jurisdiction {args.jurisdiction!r}")
    inl = ", ".join(lit(c) for c in chain)
    d = f"DATE {lit(day.isoformat())}"
    in_range = f"valid_from <= {d} AND coalesce(valid_to, DATE '9999-12-31') >= {d}"
    sections = [
        ("Governments in office",
         f"SELECT jurisdiction_id, head_name, governing_parties, support_parties, form, valid_from, valid_to "
         f"FROM v_governments WHERE jurisdiction_id IN ({inl}) AND {in_range} ORDER BY length(jurisdiction_id) DESC"),
        ("Legislatures",
         f"SELECT legislature_id, body, number, valid_from, valid_to, election_id FROM legislatures "
         f"WHERE jurisdiction_id IN ({inl}) AND {in_range}"),
        ("Seats from the election that opened each legislature",
         f"SELECT l.legislature_id, r.body, r.party_id, r.seats, r.vote_share_pct FROM legislatures l "
         f"JOIN election_results r ON r.election_id = l.election_id WHERE l.jurisdiction_id IN ({inl}) "
         f"AND l.valid_from <= {d} AND coalesce(l.valid_to, DATE '9999-12-31') >= {d} AND r.seats > 0 "
         f"ORDER BY l.legislature_id, r.body, r.seats DESC"),
        ("Latest indicator values at that date",
         f"SELECT indicator_id, name_es, jurisdiction_id, arg_max(value, period_start) AS value, unit, "
         f"max(period_start) AS period FROM v_indicators WHERE jurisdiction_id IN ({inl}) AND period_start <= {d} "
         f"GROUP BY indicator_id, name_es, jurisdiction_id, unit ORDER BY indicator_id"),
        (f"Events in the previous {args.days} days",
         f"SELECT date, jurisdiction_id, category, title FROM events WHERE jurisdiction_id IN ({inl}) "
         f"AND date BETWEEN {d} - {int(args.days)} AND {d} ORDER BY date DESC LIMIT 30"),
        ("Coverage of context data",
         f"SELECT dataset, completeness, period_from, period_to, last_checked FROM coverage "
         f"WHERE jurisdiction_id IN ({inl}) AND dataset IN ('governments', 'government_parties', 'legislatures', "
         f"'election_results', 'indicators', 'events')"),
    ]
    print(f"# context for {day.isoformat()} · jurisdiction chain: {' > '.join(reversed(chain))}")
    for title, sql in sections:
        print(f"\n## {title}")
        cur = con.execute(sql)
        rows = cur.fetchall()
        if rows:
            print_rows([c[0] for c in cur.description], rows, "csv", 200)
        else:
            print("(none recorded: check coverage before assuming there was none)")


def cmd_stale(args):
    con = connect_ro()
    run_query(con, """
        SELECT q.id AS question_id, q.updated AS answer_updated, r.related_id AS evidence_id, e.type,
               e.updated AS evidence_updated,
               CASE WHEN e.id IS NULL THEN 'evidence missing' ELSE 'evidence updated after answer' END AS reason
        FROM questions q
        JOIN entity_relations r ON r.entity_id = q.id AND r.relation = 'evidence'
        LEFT JOIN entities e ON e.id = r.related_id
        WHERE e.id IS NULL OR e.updated > q.updated
        ORDER BY q.id""", limit=500)


# ----------------------------------------------------------------------------- writing helpers
BODY_TEMPLATES = {
    "measure": {"es": ["Qué establece", "Tramitación y apoyos", "Aplicación y estado", "Evaluaciones y datos"],
                "en": ["What it does", "Passage and support", "Implementation and status", "Evaluations and data"]},
    "vote_note": {"es": ["Qué se votaba", "Resultado y posiciones", "Contexto y matices"],
                  "en": ["What was voted", "Result and positions", "Context and caveats"]},
    "statement": {"es": ["Contexto", "Verificación"], "en": ["Context", "Verification"]},
    "program": {"es": ["Resumen por tema (con páginas)"], "en": ["Summary by topic (with pages)"]},
    "dossier": {"es": ["Marco legal y competencial", "Datos clave", "Evidencia sobre este país",
                       "Posiciones y acciones de los partidos", "Huecos de datos"],
                "en": ["Legal framework and competences", "Key data", "Country evidence",
                       "Party positions and actions", "Data gaps"]},
    "history": {"es": ["Resumen", "Datos"], "en": ["Summary", "Data"]},
    "study": {"es": ["Pregunta", "Método y datos", "Resultados", "Limitaciones", "Relevancia"],
              "en": ["Question", "Method and data", "Findings", "Limitations", "Relevance"]},
    "knowledge": {"es": ["Alcance", "Mecanismos", "Evidencia por afirmación", "Debates abiertos"],
                  "en": ["Scope", "Mechanisms", "Evidence by claim", "Open debates"]},
    "question": {"es": ["Respuesta vigente", "Historial de revisiones", "Huecos detectados"],
                 "en": ["Current answer", "Revision history", "Data gaps"]},
}


def cmd_new(args):
    schema = Schema()
    tname = schema.md_by_type.get(args.type)
    if not tname:
        fail(f"unknown type {args.type!r}; valid: {sorted(schema.md_by_type)}")
    t = schema.tables[tname]
    if not re.match(t["id_pattern"], args.id):
        fail(f"id must match {t['id_pattern']}")
    country = country_of(args.id, known_countries())
    folder = ROOT / t["folder"].replace("{country}", country)
    if args.dir:
        if not t.get("free_subfolders"):
            fail(f"--dir is only allowed for types stored in free subfolders")
        folder = folder / args.dir
    path = folder / f"{args.id}.md"
    if path.exists():
        fail(f"{rel(path)} already exists")
    lang = args.lang or (COUNTRY_LANG.get(country, "en") if "{country}" in t["folder"] else "en")
    preset = {"id": args.id, "type": args.type, "lang": lang, "created": today(), "updated": today(),
              "date_precision": "day"}
    lines = ["---"]
    for c, spec in t["all_columns"].items():
        hint = []
        if spec.get("required"):
            hint.append("required")
        if spec.get("fk"):
            hint.append(f"→ {spec['fk']}")
        if spec.get("values") and c not in ("type", "lang"):
            hint.append(" | ".join(map(str, spec["values"])))
        elif spec["type"] in ("date", "int", "float", "bool", "url"):
            hint.append(spec["type"])
        if spec.get("max_len"):
            hint.append(f"max {spec['max_len']} chars")
        value = preset.get(c, "")
        lines.append((f"{c}: {value}".rstrip() + ("  # " + "; ".join(hint) if hint and not value else "")).rstrip())
    for lf, ls in t["all_lists"].items():
        lines.append(f"{lf}: []  # {list_hint(schema, ls)}")
    lines += ["---", ""]
    heads = BODY_TEMPLATES.get(args.type, {}).get("es" if lang == "es" else "en", [])
    for h in heads:
        lines += [f"## {h}", "", ""]
    folder.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8", newline="\n")
    print(rel(path))


def csv_value(v) -> str:
    if v is None:
        return ""
    if isinstance(v, bool):
        return "true" if v else "false"
    return str(v)


def resolve_path(t, row, countries) -> Path:
    def rep(m):
        name = m.group(1)
        if name == "country":
            for c in (t["key"][0], "entity_id", "jurisdiction_id"):
                v = row.get(c)
                if v and country_of(str(v), countries) != "global":
                    return country_of(str(v), countries)
            raise ValueError("cannot infer {country}")
        v = row.get(name)
        if not v:
            raise ValueError(f"cannot infer {{{name}}}")
        return str(v)
    try:
        return ROOT / re.sub(r"\{([^}]+)\}", rep, t["path"])
    except ValueError as e:
        fail(f"{t['name']}: {e} from the row; pass --file")


def append_csv(path: Path, t, row) -> None:
    cols = list(t["all_columns"])
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.stat().st_size > 0:
        hdr = read_header(path)
        if set(hdr) != set(cols):
            fail(f"{rel(path)}: header differs from schema; fix the file first")
        with path.open("rb") as f:
            f.seek(-1, os.SEEK_END)
            needs_newline = f.read(1) != b"\n"
        with path.open("a", encoding="utf-8", newline="") as f:
            if needs_newline:
                f.write("\n")
            csv.writer(f, lineterminator="\n").writerow([csv_value(row.get(c)) for c in hdr])
    else:
        with path.open("w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(cols)
            w.writerow([csv_value(row.get(c)) for c in cols])


def cmd_add(args):
    schema = Schema()
    t = schema.tables.get(args.table)
    if not t or t["kind"] not in ("csv", "link"):
        fail(f"{args.table!r} is not a CSV table; CSV tables: {sorted(x['name'] for x in schema.of_kind('csv', 'link'))}")
    try:
        data = json.loads(sys.stdin.read() if args.json == "-" else args.json)
    except json.JSONDecodeError as e:
        fail(f"invalid JSON: {e}")
    rows = data if isinstance(data, list) else [data]
    countries = known_countries()
    list_fields = schema.common["lists"] if t.get("entity") else {}
    written: dict[str, int] = {}
    pending = []
    for row in rows:  # check every row before writing any, so a bad row leaves no partial write
        if not isinstance(row, dict):
            fail("each row must be a JSON object")
        links = {lf: row.pop(lf) for lf in list(row) if lf in list_fields}
        unknown = [k for k in row if k not in t["all_columns"]]
        missing = [c for c, s in t["all_columns"].items() if s.get("required") and row.get(c) in (None, "")]
        if unknown or missing:
            fail(f"row {row}: unknown columns {unknown}, missing required {missing}; nothing was written")
        path = Path(args.file).resolve() if args.file else resolve_path(t, row, countries)
        pending.append((row, links, path))
    for row, links, path in pending:
        append_csv(path, t, row)
        written[rel(path)] = written.get(rel(path), 0) + 1
        eid = row[t["key"][0]]
        for lf, items in links.items():
            ls = list_fields[lf]
            target = schema.tables[ls["table"]]
            for item in items if isinstance(items, list) else [items]:
                r = {"entity_id": eid, **(ls.get("defaults") or {})}
                if isinstance(item, dict):
                    r.update(item)
                else:
                    r[ls["scalar_column"]] = item
                p = resolve_path(target, r, countries)
                append_csv(p, target, r)
                written[rel(p)] = written.get(rel(p), 0) + 1
    for p, n in written.items():
        print(f"added {n} row(s) to {p}")


def cmd_scaffold(args):
    schema = Schema()
    created = []
    for t in schema.of_kind("csv", "link"):
        names = re.findall(r"\{([^}]+)\}", t["path"])
        if names and names != ["country"]:
            continue
        for country in (args.country if names else [None]):
            p = ROOT / (t["path"].replace("{country}", country) if country else t["path"])
            if not p.exists():
                p.parent.mkdir(parents=True, exist_ok=True)
                with p.open("w", encoding="utf-8", newline="") as f:
                    csv.writer(f, lineterminator="\n").writerow(list(t["all_columns"]))
                created.append(rel(p))
    print("\n".join(f"created {p}" for p in created) or "nothing to create")


# ----------------------------------------------------------------------------- CLI
def main(argv=None):
    ap = argparse.ArgumentParser(prog="kb", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build", help="validate and rebuild the database")
    sub.add_parser("validate", help="validate sources without building")
    p = sub.add_parser("sql", help="read-only SQL query")
    p.add_argument("query", help="SQL text, or '-' to read it from stdin")
    p.add_argument("--limit", type=int, default=100, help="max rows printed (default 100)")
    p.add_argument("--format", choices=["csv", "md", "json"], default="csv")
    p.add_argument("--width", type=int, default=300, help="truncate cells longer than this (default 300)")
    p.add_argument("--full", action="store_true", help="do not truncate cells")
    p = sub.add_parser("search", help="full-text search")
    p.add_argument("query")
    p.add_argument("--type", help="restrict to an entity type (measure, study, knowledge, event, vote...)")
    p.add_argument("--lang", help="restrict to a language (es, en...)")
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--format", choices=["csv", "md", "json"], default="csv")
    p = sub.add_parser("context", help="political and economic context at a date")
    p.add_argument("date")
    p.add_argument("--jurisdiction", default="es")
    p.add_argument("--days", type=int, default=180, help="window for recent events (default 180)")
    p = sub.add_parser("schema", help="describe tables")
    p.add_argument("tables", nargs="*")
    p = sub.add_parser("new", help="create a Markdown entity")
    p.add_argument("type")
    p.add_argument("id")
    p.add_argument("--dir", help="subfolder (knowledge only), e.g. economics/housing_market")
    p.add_argument("--lang")
    p = sub.add_parser("add", help="append rows to a CSV table")
    p.add_argument("table")
    p.add_argument("--json", required=True, help="JSON object or list of objects, or '-' for stdin")
    p.add_argument("--file", help="target CSV (needed when the path cannot be inferred)")
    sub.add_parser("stale", help="questions whose evidence changed")
    p = sub.add_parser("scaffold", help="create missing CSV files with headers")
    p.add_argument("--country", nargs="+", default=["es"])
    args = ap.parse_args(argv)

    if args.cmd == "build":
        sys.exit(build(write=True))
    if args.cmd == "validate":
        sys.exit(build(write=False))
    if args.cmd == "schema":
        print(schema_text(Schema(), args.tables))
        return
    {"sql": cmd_sql, "search": cmd_search, "context": cmd_context, "new": cmd_new, "add": cmd_add,
     "stale": cmd_stale, "scaffold": cmd_scaffold}[args.cmd](args)


if __name__ == "__main__":
    main()

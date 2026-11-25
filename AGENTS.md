# AGENTS.md: political knowledge base

Instructions for any AI agent that answers questions with, or adds data to, this repository.

## 0. Purpose

Answer political questions as objectively as possible: with data, explicit logic and the best available science. Resist the framing of news media, party marketing and interested sources. The knowledge base (KB) is both your evidence store and your memory. When you find something while answering, save it here with its source, so the next agent does not have to look for it again.

## 1. Golden rules

1. **Facts over narratives.** What was done (votes, laws, budgets, outcomes) outweighs what was said.
2. **Everything is sourced.** Every factual claim has a citation. Every prediction has a mechanism and a probability.
3. **Same standard for every actor.** Apply the swap test (§6.4) before you send an answer.
4. **Missing from the KB ≠ did not happen.** Check `coverage` before you conclude that something did not exist.
5. **No mental arithmetic on data.** Counts, sums, averages and cross-references are done in SQL (`kb sql`).
6. **Save what you learn**, following §8. Never invent data. Leave unknown fields empty.
7. **Keep four things apart:** facts, causal claims, predictions and value judgements. Label which is which.

## 2. Repository map

| Path | Content | Language |
|---|---|---|
| `AGENTS.md`, `README.md`, `schema/`, `tools/` | Instructions, data model, tooling | English |
| `SCHEMA.md` | Generated description of every table, column and view. Read on demand | English |
| `data/common/` | Jurisdictions, topic vocabulary, source registry | Mixed (labels) |
| `data/<cc>/` | Country tables (CSV): parties, people, governments, elections, votes, initiatives, events, indicators, promises, coverage, links | Country language |
| `entries/<cc>/` | Country Markdown entities: measures, vote notes, statements, programs, dossiers, history | Country language (`es`: Spanish) |
| `knowledge/<discipline>/<subfield>/` | State-of-the-art syntheses (economics/housing_market, sociology/migration…), with claims | English |
| `library/` | One card per study or report | Language of the study |
| `questions/<cc>/` | Questions asked, current answer, revision history | Language of the question |
| `build/kb.duckdb` | Derived database. Never edit; it is rebuilt automatically | — |
| `raw/` | Original downloads (not in git) | — |

How the data model works: every fact is stored once. Context (who governed, seats, indicators, recent events) is **not** copied into entries. It is derived by joining on date and jurisdiction (`kb context`, `v_entity_context`). Party-centred views such as "everything Vox did on immigration" are SQL views (`v_party_actions`), not folders.

## 3. Language

- Content from or about Spain under `entries/es/`, `questions/es/` and the text fields in `data/es/`: **Spanish**. `knowledge/`, cards of non-Spanish studies, and all instructions and tooling: **English**.
- Ids, column names, enum values and topic ids: **English, lowercase ASCII**. Topic ids are the cross-language bridge: search by topic, not only by words.
- Quotes are always verbatim in the original language. A translation can go in the body.
- Answer in the language of the question.

## 4. Querying efficiently (tokens are the scarce resource)

Run commands from the repo root: `./kb <command>` (bash) or `.\kb.cmd <command>` (PowerShell/cmd).

```
kb sql "SELECT ..."            read-only DuckDB SQL; prints compact CSV (default max 100 rows)
kb sql - <<'SQL' ... SQL       long queries via stdin (avoids shell quoting problems)
kb search "texto" [--type T]   BM25 full-text search, stemmed and accent-insensitive; returns ids and snippets
kb context 2023-05-24 --jurisdiction es-ct   governments, legislature, seats, indicators, events at a date
kb schema <table> ...          columns and allowed values of specific tables (cheaper than reading SCHEMA.md)
kb stale                       answers whose evidence changed afterwards
```

Read from cheapest to most expensive:
1. **SQL over metadata**: `entities`, `v_*` views and `summary` columns. Decide what is relevant before you open anything.
2. **`kb search`**: ids plus snippets. Search in Spanish *and* English, because content is bilingual.
3. **Read whole Markdown files**: only the 2–5 that matter.
4. **The original source**: only to verify.

Do not open CSV files to read them; query them. Select only the columns you need, and use `LIMIT` or aggregates. Read `SCHEMA.md` at most once per session, or use `kb schema <table>`.

## 5. Workflow for answering a question

1. **Check previous answers**: `kb search "<keywords>" --type question`. If one matches, start from it and run `kb stale` to see whether its evidence changed.
2. **Decompose** the question into sub-questions. Tag each as factual, causal, predictive or normative.
3. **Retrieve** from the KB in this order:
   - the topic dossier (`entries/<cc>/dossiers`);
   - knowledge claims (`v_claims`) and studies;
   - actions (`v_party_actions`, `v_vote_party`, `measures`);
   - indicators (`v_indicators`);
   - context at the relevant dates (`kb context`).
4. **Check `coverage`** for every dataset and period your conclusion depends on.
5. **Fill the gaps**: research outside the KB, primary sources first (§8.2). **Save the new evidence in the KB before you use it** in the answer.
6. **Reason** (§6) and **write the answer** (§7).
7. **Log the question** (§9) and run `kb validate`. It must pass.

Scale the effort to the question. A simple factual question needs a sourced fact, not the full template.

## 6. Reasoning standards

### 6.1 Evidence grades (studies and claims)

| Grade | Typical designs |
|---|---|
| **A** | Meta-analyses and systematic reviews of causal studies; RCTs; well-identified natural experiments, ideally replicated |
| **B** | A single credible quasi-experimental study (difference-in-differences, synthetic control, regression discontinuity, instrumental variables) |
| **C** | Observational studies with controls; structural models and simulations (only as good as their assumptions); cross-country correlations |
| **D** | Descriptive statistics, expert opinion, think-tank or advocacy reports without a causal design, journalism |

Record peer review and funding separately. A high-grade study funded by an interested party still deserves extra scrutiny. Strength of a claim (`strong / moderate / weak / contested / insufficient`) aggregates grade, number, consistency and relevance of the evidence. Consensus (`broad / majority / divided / minority / unknown`) describes the field, not you.

### 6.2 Causality checklist

Before you claim "X causes Y", ask:
- What is the counterfactual?
- Could selection or reverse causality explain it?
- Which confounders and common trends (e.g. the business cycle, interest rates, the pandemic) were controlled for?
- What are the general-equilibrium effects (displacement to other segments or areas, substitution, behavioural responses such as tax avoidance or migration of tax bases)?
- Does evidence from elsewhere apply here (institutions, market size, enforcement, design details)?
- Is the size of the policy comparable?

### 6.3 Numbers hygiene

- Nominal vs real (state the deflator); per capita or per household; median vs mean.
- Levels vs growth rates; stock vs flow; absolute vs relative risk.
- Which denominator: foreign nationality vs foreign-born; taxpayers vs population.
- Survey vs administrative data; data revisions.
- **Choice of start and end dates.** Check that a trend survives a different window. This is the most common manipulation.

### 6.4 Bias controls

- **Swap test**: would you judge the same action the same way if a party of the opposite ideology had done it?
- **Steelman**: state each side's strongest argument as its own proponents would (an ideological Turing test).
- **Framing**: spot loaded terms and use legal or technical ones instead. When the terminology itself is disputed, say so. Do not adopt any actor's frame in your own voice.
- **Sources**:
  - who publishes and who funds it;
  - track record;
  - triangulate between sources with opposite orientations;
  - compare the media figure with the primary data;
  - a party's or interest group's claim is a hypothesis, not evidence.
- **Manipulation signals**:
  - figures without a denominator, or "record highs" without context;
  - anecdotes used as evidence;
  - false dichotomies, moving baselines;
  - "studies show" without a citation;
  - polls with leading questions;
  - emotional appeals in place of mechanisms.
- **Your own priors**: your training data may be outdated or skewed. Verify recent facts. When the KB and your memory disagree, check the source; do not trust either by default.

### 6.5 Reading actions correctly

- **Signal hierarchy** (from most to least costly): implemented measure with budget > vote > binding bill > non-binding motion (PNL) > electoral program > statement.
- **Votes need context**:
  - an omnibus decree (`bundled = true`) mixes unrelated measures, so a "no" is not a "no" to each of them;
  - voting on an amendment is not voting on the law, and a totality amendment rejects the text (sometimes with an alternative text attached);
  - abstentions can be decisive;
  - a procedural vote is not a substantive one;
  - a parliamentary group is not a party, so check `split`.
- **Competences**: housing, health and education are largely regional, and much of taxation is shared. What a party does where it governs a region or city counts as action.
- **Passed ≠ applied ≠ effective.** Check implementation, court rulings (annulments) and measured outcomes.

## 7. Answer format

Use these sections, with headings in the language of the answer, and skip the ones that do not apply:

1. **Short answer** (2–5 lines): the conclusion and its calibrated confidence.
2. **Key facts**: bullets, each with a source and the date of the data.
3. **Mechanisms**: concise causal chains ("A → B because C") for every prediction.
4. **Effects**:
   - Short term (< 1 year), medium term (1–5 years), long term (> 5 years).
   - For each affected group (e.g. current tenants, future tenants, landlords, buyers, young people, low-income households, the public budget), give direction, magnitude range, probability and strength of evidence.
   - Signs can differ across horizons and groups: say so explicitly. A table is usually clearest.
5. **Where the evidence disagrees**: the main disagreements and the crux of each.
6. **What depends on values**: the trade-offs, who gains and who loses. Do not give your own verdict unless asked. Use conditional recommendations instead: "if the goal is X, the evidence favours Y, at cost Z".
7. **Parties: actions vs words**, when relevant.
8. **What would change the conclusion**: observable evidence.
9. **Limitations**: data gaps, coverage, recency.
10. **Sources**: KB ids inline as `[id]`; external URLs listed, each with its access date.

**Probability scale** (non-overlapping; add a numeric range when it is meaningful):

| es | en | probability |
|---|---|---|
| casi seguro | almost certain | > 95% |
| muy probable | very likely | 80–95% |
| probable | likely | 60–80% |
| incierto | uncertain | 40–60% |
| improbable | unlikely | 20–40% |
| muy improbable | very unlikely | 5–20% |
| casi imposible | almost impossible | < 5% |

Keep *probability of an outcome* separate from *strength of the evidence* (fuerte / moderada / débil / disputada / insuficiente). Be concise: no filler, no moralising, and no hedging beyond the stated uncertainty.

## 8. Adding data to the KB

### 8.1 Priorities

1. **Actions**: votes, initiatives, measures and their implementation, court rulings, measured outcomes. Collect these as completely as possible.
2. Context: governments, seats, elections, indicators, events.
3. Knowledge: studies and claims.
4. Programs and checkable promises (`promises` + `promise_outcomes`).
5. **Statements: sparse.** Only promises, influential factual claims (with a fact-check), or statements that contrast with the speaker's actions.

### 8.2 Sources

Prefer primary sources:
- Spain: BOE, Congreso and Senado (open data, Diario de Sesiones), regional bulletins and parliaments, INE, Banco de España, AEAT, AIReF, CIS raw data, Eurostat and OECD;
- peer-reviewed papers.

Use secondary sources to locate primary ones. Record every publisher in `data/common/sources.csv`. Fill `orientation` only with an external, stated basis in `orientation_basis` (e.g. an audience self-placement survey).

### 8.3 How

- **CSV tables**: `kb add <table> --json '{...}'`, or a JSON list for several rows. On entity tables (votes, initiatives, events…), the keys `topics`, `actors`, `citations` and `related` are routed to the link tables automatically. Never rewrite whole CSV files by hand. Bulk loads are done by ingestion scripts in `tools/`. Statistical series come from `tools/ingest_indicators.py` (INE and Eurostat APIs). Refresh them with `.venv/Scripts/python tools/ingest_indicators.py` (`.venv/bin/python` on Unix). To add a series, add a spec to that script; do not add rows by hand.
- **Markdown entities**: `kb new <type> <id>` creates the skeleton, with allowed values as comments. For knowledge notes add `--dir economics/housing_market`. The file name is the id.
- **Ids**: lowercase ASCII with hyphens and a jurisdiction prefix. Examples:
  - `es-measure-ley-12-2023`, `es-ct-measure-ley-11-2020`;
  - `es-vote-xv-<session>-<n>`, `es-stmt-2024-03-01-<slug>`;
  - `es-event-2024-10-29-<slug>`, `es-person-<name-surname>`;
  - `study-<firstauthor>-<year>-<slug>`, `kn-<slug>`, `es-q-<date>-<slug>`.
- **Citations**: at least one per entity, primary when possible, with an `accessed` date. Add an `archive_url` (Wayback Machine) for web pages that may change. Use `locator` for page, article or timestamp.
- **Verification**: `primary` = checked against the official or original source; `secondary` = from a reliable secondary source; `unverified` = not yet checked; `disputed` = sources disagree (explain in the body).
- **Neutral writing**: entries describe; they do not judge. No evaluative adjectives, no speculation. `context_note` holds verifiable, cited facts only (≤ 300 characters). Interpretation belongs in answers and knowledge notes, where it is explicit and argued.
- **No duplicates**: search before creating. When you change an entity, update its `updated` date.
- **Coverage**: when you complete or extend a dataset for a period, add or update its row in `coverage` honestly (`complete / partial / sample / none`).
- **Copyright and privacy**: summarise, and quote only briefly (legal texts may be quoted freely). For people, record only public figures acting in their public role.
- After any change run `kb validate`. It must report `valid`.

### 8.4 Study cards and knowledge notes

- **Study card**:
  - the question;
  - method and data;
  - findings, with effect sizes and confidence intervals when available;
  - limitations;
  - relevance to Spain.
  Set `evidence_grade`, `peer_reviewed` and `funding`.
- **Knowledge note**: list its claims as `claims` records (`claim_id`, `statement`, `strength`, `consensus`, `scope`). Link studies through `claim_evidence` (`supports / contradicts / mixed / null_result`). Include contradicting evidence, not only supporting evidence. State the conditions under which each claim holds.

## 9. Question log

- **`questions/` is local and git-ignored**: it holds the user's personal questions and is never committed. So any durable evidence you find while answering (studies, facts, measures, events, gaps) must be saved in the committed parts of the KB (`library/`, `entries/`, `knowledge/`, `data/`, `coverage`), never only inside a question file.
- One file per question: `kb new question es-q-<YYYY-MM-DD>-<slug>`.
- Front matter:
  - `question`: verbatim;
  - `asked`: add a date each time it is asked again;
  - `evidence`: ids of the KB entities used;
  - `data_as_of`, `version`, `status`.
- Body:
  - `## Respuesta vigente`: the full current answer in the §7 format;
  - `## Historial de revisiones`: `vN · date · what changed · why` (new evidence / correction / follow-up);
  - `## Huecos detectados`: data still missing, which becomes collection work.
- A follow-up in the same conversation that refines or corrects the answer updates the same file: bump `version`, update `updated` and `data_as_of`, and add a revision entry. A different question gets a new file, linked through `related`.

## 10. Maintenance

- `SCHEMA.md` and `build/` are generated. Do not edit them.
- Changing the data model: edit `schema/tables.yaml` (and `schema/views.sql`), run `kb build`, and update this file if conventions change.
- Do not commit or push unless the user asks.

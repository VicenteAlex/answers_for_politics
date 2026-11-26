# Answers for politics

![Congress votes](https://img.shields.io/badge/Congress_votes-8%2C758-1f6feb) ![Deputy votes](https://img.shields.io/badge/individual_deputy_votes-3.06M-1f6feb) ![Studies](https://img.shields.io/badge/study_cards-142-2da44e) ![Claims](https://img.shields.io/badge/graded_claims-64-2da44e) ![Laws and measures](https://img.shields.io/badge/laws_%26_measures-47-8250df) ![Series](https://img.shields.io/badge/statistical_series-53-8250df) ![Events](https://img.shields.io/badge/events-261-8250df) ![Code AGPL-3.0](https://img.shields.io/badge/code-AGPL--3.0-lightgrey) ![Data CC BY-SA 4.0](https://img.shields.io/badge/data-CC_BY--SA_4.0-lightgrey)

An evidence base about politics that AI agents use as context to answer political questions with data, explicit logic and calibrated uncertainty. **Initialised with Spanish politics (`es`).**

Una base de evidencia sobre política para que agentes de IA respondan preguntas políticas con datos, lógica explícita e incertidumbre calibrada. **Inicializado con política española (`es`).**

## Ejemplos de respuestas · Example answers (in Spanish)

Cuatro preguntas reales, respondidas por un agente con esta base y revisadas por un segundo agente independiente en busca de sesgos y errores. Pulsa una pregunta para ver la respuesta corta; dentro está el enlace a la respuesta completa con datos, mecanismos, efectos por grupo, acciones de los partidos y fuentes.

*Four real questions, answered by an agent using this knowledge base and checked by a second, independent agent for bias and errors. Click a question for the short answer; the link inside opens the full answer.*

<details>
<summary><b>¿Hay evidencia de que las políticas de izquierdas de los últimos 10 años hayan aumentado o disminuido la criminalidad en las calles de España?</b></summary>

No hay evidencia causal suficiente para afirmar que las políticas de los gobiernos PSOE (2018-20), PSOE-UP (2020-23) y PSOE-Sumar (2023-) hayan aumentado ni reducido la delincuencia en la calle. Ninguna de esas políticas tiene un estudio con diseño causal en España sobre delincuencia callejera. Los datos descriptivos muestran tendencias mixtas:
- robos y hurtos por habitante en niveles parecidos a 2016-2019;
- suben el homicidio registrado (cifras pequeñas), los delitos sexuales registrados y la cibercriminalidad.

Confianza: es **improbable** (20-40%) que estas políticas, en conjunto, hayan movido la delincuencia callejera más de un 10% en alguna dirección. Es un juicio, no una estimación: con datos agregados no se puede separar su efecto del de otros factores (COVID, crecimiento de la población, turismo, actuación policial), que podrían compensarse. La evidencia es **débil** en general y **disputada** en política por política.

→ [Respuesta completa: datos, mecanismos, efectos por grupo, partidos y fuentes](examples/es/criminalidad-politicas-izquierda.md)

</details>
<br/><br/>
<details>
<summary><b>¿Las regulaciones de vivienda actuales han mejorado o empeorado la capacidad de los trabajadores para acceder al alquiler y a la compra?</b></summary>

El acceso a la vivienda de los trabajadores ha empeorado en la última década. La causa principal es una oferta que no sigue a la demanda (hogares nuevos, población, crédito), y no es atribuible a una regulación concreta. El efecto de las regulaciones depende del grupo:
- **Inquilinos con contrato**: mejoran (**muy probable**, evidencia **fuerte** sobre el precio). Los topes a la actualización y los contratos de 5/7 años abaratan y estabilizan su alquiler; el coste es menos movilidad.
- **Quien busca alquiler en zonas con topes**: efecto neto **incierto** (evidencia **disputada**). Quien firma paga algo menos. Es **probable** que haya menos contratos nuevos y más alquiler de temporada, pero los estudios no coinciden en cuánto. Que los topes a la actualización encarezcan las rentas de entrada es una hipótesis del Banco de España (evidencia **débil**).
- **Quien quiere comprar**: la regulación del alquiler pesa poco. Influyen más la oferta, el crédito (entrada del 20%) y la demanda. Es **probable** que las ayudas a la compra se trasladen en parte al precio donde la oferta es rígida (evidencia **moderada**, de fuera de España).

→ [Respuesta completa: datos, mecanismos, efectos por grupo, partidos y fuentes](examples/es/vivienda-regulacion-acceso.md)

</details>
<br/><br/>
<details>
<summary><b>¿Qué leyes sanitarias aprobó el último Gobierno del PSOE frente al último del PP? ¿Con quién ha sido mejor el acceso de la población a la sanidad?</b></summary>

- **Legislación (hecho, BOE).** El Gobierno Rajoy (PP, dic. 2011-jun. 2018) **restringió** el derecho y la gratuidad: condición de "asegurado" (inmigrantes adultos sin papeles limitados a urgencias, embarazo y parto), copago para pensionistas y recortes de personal y gasto, en plena crisis de deuda; también financió los antivirales de la hepatitis C (2015). El Gobierno Sánchez (PSOE y coaliciones, jun. 2018-2026) **amplió**: acceso universal, exenciones de copago, cartera dental, eutanasia y Agencia de Salud Pública.
- **Acceso.** No hay un ganador limpio; depende del indicador:
  - *Derecho legal a la asistencia*: más amplio con el PSOE (casi seguro, es un hecho normativo).
  - *Barreras por coste*: máximas en 2011-2014 (crisis y copago), pero ya bajas en 2015-2018, aún con el PP. Fuera de la crisis, la diferencia es pequeña.
  - *Esperas*: niveles más altos con el PSOE, y la necesidad no cubierta por espera se multiplicó desde 2020 (probable que el acceso efectivo fuera peor en 2020-2025). Pero en ventanas sin rotura de serie ambos periodos empeoran en algún indicador, y las listas son autonómicas: la atribución al Gobierno central es débil.

| Ventana | Días de espera media | Pacientes por 1.000 | % > 6 meses |
|---|---|---|---|
| PP, jun. 2012 → dic. 2015 | 76 → 89 (+17%) | 11,8 → 12,2 | 9,4 → 10,6 |
| PSOE, dic. 2018 → dic. 2025 | 129 → 122 (−5%) | 14,8 → 17,7 (+20%) | 20,0 → 21,6 |

→ [Respuesta completa: datos, mecanismos, efectos por grupo, partidos y fuentes](examples/es/sanidad-psoe-vs-pp.md)

</details>
<br/><br/>

<details>
<summary><b>Ante la pérdida de empleo por la automatización con IA, ¿pueden las leyes laborales cambiar el impacto en los trabajadores? ¿Qué proponen y han aprobado derechas e izquierdas, y qué efectos cabe esperar según la evidencia?</b></summary>

**Sí, pero sobre todo cambian *quién* soporta el ajuste y *a qué ritmo*, no cuánta automatización llega.** Hasta 2026 los efectos causales medidos de la IA sobre el empleo agregado son pequeños o nulos; las señales negativas (jóvenes, EE. UU.) son descriptivas.

- **PP (2012):** abarató el despido y amplió la flexibilidad interna (convenio de empresa, descuelgues, ERE/ERTE sin autorización).
- **PSOE-UP (2021):** restringió la temporalidad, creó el Mecanismo RED, reforzó el convenio sectorial, dio derechos de información sobre algoritmos y subió el SMI; no tocó la indemnización.
- **2026:** nadie propone abaratar el despido; la izquierda propone encarecerlo y el PP, formación portable.

Nadie ha aplicado recolocación específica para la IA. **Predicción condicional:** con difusión rápida, los más perjudicados serían los jóvenes que entran en ocupaciones expuestas (*probable*) y los administrativos veteranos que sean despedidos (despidos masivos *inciertos*; si ocurren, pérdidas grandes *muy probables*). Evidencia moderada sobre mecanismos, débil sobre la incidencia de la IA.

→ [Respuesta completa: datos, mecanismos, efectos por grupo, partidos y fuentes](examples/es/ia-automatizacion-leyes-laborales.md)

</details>
<br/><br/>

<details>
<summary><strong><big><big>English README</big></big></strong></summary>

## What it is

A knowledge base of political facts, actions and research. AI agents use it to answer political questions objectively: with data, explicit logic and the best available science. It started with **Spanish politics**; the structure is ready for other countries (see *Adding a country*). Agent instructions are in [AGENTS.md](AGENTS.md).

Current content for Spain:
- **Political context:** governments since 1977, regional governments since 2015, Barcelona and Madrid since 2011.
- **Elections and parliament:** election results and legislatures.
- **Parliament:** all 8,758 electronic plenary votes of the Congreso in the XIV and XV legislatures (2019–2026), with each deputy's vote.
- **Events:** about 260 events.
- **Statistics:** 53 INE and Eurostat series (labour market, prices, housing, crime, health, population, public finances…).
- **In-depth topics:** rent regulation, immigration, wealth taxation, crime, health care, and AI and labour law. They hold 142 study cards, 9 knowledge notes with 64 graded claims, 3 Spanish dossiers, 47 laws and measures, and the 2023 and 2026 programmes of the main national parties on labour.
- **Answered questions:** seven answered and independently reviewed for bias; four are shown as examples above.

## Why use it: an honest assessment

This assessment is based on the first three answers, on rent caps in Barcelona, Vox/PP immigration policies and taxes on large fortunes.

**What it adds over asking a chatbot directly**
- **Traceable answers.** Each answer cites 33–53 KB entities inline, and figures are computed with SQL instead of mentally. An independent reviewer re-checked 14 figures in one answer and found no errors.
- **Current, local facts the model does not know.** Examples: the October 2026 dissolution of the Cortes, the 2026 regularisation decree, the housing decrees rejected in 2026, and the 2026 PP–Vox regional pacts. A model without the base would miss or invent these.
- **Discipline.** Answers keep facts, causal claims, predictions and value judgements apart. They give effects by time horizon and by affected group, use a fixed probability scale, and list gaps explicitly. A `coverage` table stops agents from treating "not in the KB" as "did not happen".
- **Bias correction that demonstrably works.** An independent review pass found real problems in every first draft:
  - the first immigration answer omitted the strongest evidence for restriction and applied caveats to one side only;
  - the wealth-tax answer misdated the dissolution of the Cortes;
  - the rent answer left out the policy's intended benefit.

  All of them were corrected in version 2. Most of the value comes from this loop (data → answer → adversarial review → revision), not from the instructions alone.
- **Cumulative and cheap at the margin.** Building the context and the three topics cost at least 2.4M tokens of agent work. After that, each new question in a covered topic cost about 250k tokens and 5–10 minutes, review included. Follow-up questions update the same answer file and keep a revision history.

**Limitations you should know**
- **The evidence base is still thin and partly secondary.**
  - Of 142 study cards, 81 are grade A/B, and 80 are marked "secondary" (often checked from an abstract or working paper).
  - Spanish causal studies are scarce, 4–7 per answer, so many conclusions transfer evidence from the US or Germany.
  - Several party programmes were read from copies hosted by media outlets.
- **Party votes.** Electronic Congreso votes since 2019 come from official open data; roll-call votes, the Senate, regional parliaments and older votes still come from press reports.
- **One model writes and reviews.** Blind spots are correlated. The reviewer itself proposed legal citations from memory, which then had to be verified. No human expert has reviewed the content yet.
- **Selection and anchoring.** The research briefs named key studies, so the literature reflects whoever wrote the prompts as well as what the agents found.
- **Probabilities are reasoned judgements, not models.** There is no calibration track record yet.
- **"Valid" means well-formed, not true.** The validator checks structure and references, not facts.
- **Answers are long** (2,100–2,600 words). Ask for the short answer only if that is what you need.
- **Depth is limited to the topics researched.** A new topic needs a research pass of about 300–450k tokens per topic before answers are reliable.

**Bottom line.** It is an auditable briefing tool, not an oracle and not peer-reviewed research. Use it when you want to know what the evidence says, how sure we can be and where it comes from. It is weaker where no good evidence exists; in that case it should say so explicitly.

**Recommended improvements**
- Make the independent review a mandatory step in AGENTS.md.
- Log predictions so they can be scored later (calibration).
- Have humans spot-check a sample of claims.
- Ask agents to search adversarially for the strongest evidence against each main claim.

## How to use it

**Install** (Python 3.10+):

```bash
git clone --depth 1 https://github.com/VicenteAlex/answers_for_politics.git && cd answers_for_politics
python3 -m venv .venv && .venv/bin/python -m pip install -r requirements.txt && ./kb build
```

On Windows: `python -m venv .venv`, `.\.venv\Scripts\python -m pip install -r requirements.txt`, `.\kb.cmd build`. Details in *Setup*.

1. Open an agent with shell access (Claude Code, Codex…) in this folder. It reads `AGENTS.md` (Claude Code through `CLAUDE.md`).
2. Ask your question in any language. The agent:
   - checks previous answers;
   - queries the KB;
   - researches and saves missing evidence;
   - answers in the standard format;
   - logs the question in `questions/<country>/`. This folder is git-ignored: your questions and answers stay on your machine, while the evidence gathered to answer them goes into the committed KB.
3. For sensitive topics, ask for an independent bias review of the answer and for a revised version.
4. Follow-up questions refine the same answer file (version and revision history). Run `kb stale` to find answers whose evidence changed.
5. Review changes with `git diff` before committing.

## Design

- **Plain text files are the source of truth**:
  - CSV for tabular and bulk data (`data/`);
  - Markdown with YAML front matter for entities that carry text (`entries/`, `knowledge/`, `library/`, `questions/`).
- **Normalised relational model**, defined in [schema/tables.yaml](schema/tables.yaml):
  - every fact is stored once;
  - many-to-many relations (topics, parties, citations, evidence) live in link tables;
  - time-bounded tables (governments, party links, roles) carry `valid_from` / `valid_to`.
- **Context is derived, not copied.** Who governed, the seats and the indicators at a given date come from ASOF joins on date and jurisdiction.
- **A derived database**, `build/kb.duckdb`, is rebuilt from the files in seconds and is not stored in git. Agents query it with SQL through a CLI. An MCP server is not needed while agents have a shell; `tools/kb.py` can be wrapped in one later.
- **Querying is token-efficient**: agents run SQL over metadata, then full-text search, then read whole files only when needed.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\kb.cmd build
```

On Linux or macOS: `python3 -m venv .venv && .venv/bin/python -m pip install -r requirements.txt && ./kb build`. On first build, DuckDB downloads its official `fts` (full-text search) extension.

**Lighter clones.** The data is small (about 24 MB checked out), and git already compresses it when you clone or pull. If bandwidth or disk is tight:

```bash
# only the current version, without history
git clone --depth 1 <repository-url>

# also skip each deputy's vote (data/es/vote_casts/), keeping everything else
git clone --depth 1 --filter=blob:none --sparse <repository-url>
cd <repository-folder>
git sparse-checkout set --no-cone '/*' '!/data/es/vote_casts/'
```

Skip `vote_casts` only if you don't need vote analysis. Party positions in each vote (`vote_results`, `v_vote_party`) are computed from it, so without it those views are empty.

## Commands

| Command | What it does |
|---|---|
| `kb build` / `kb validate` | Validate sources (types, allowed values, keys, foreign keys, id patterns, file locations) and rebuild the database |
| `kb sql "<SQL>"` | Read-only query; rebuilds automatically when sources have changed |
| `kb search "<text>"` | BM25 search over titles, summaries and bodies (Spanish and English stemming) |
| `kb context <date> --jurisdiction <id>` | Governments, legislature, seats, indicators and recent events at a date |
| `kb new <type> <id>` / `kb add <table> --json ...` | Create a Markdown entity / append CSV rows (including links) |
| `kb stale` | Answers whose evidence changed after they were written |
| `kb schema [table]` | Data model description ([SCHEMA.md](SCHEMA.md) is generated by `build`) |
| `.venv/Scripts/python tools/ingest_indicators.py [--only id ...]` | Download and refresh the statistical series from the INE and Eurostat APIs (`--list` shows them) |

## Layout

```
AGENTS.md  CLAUDE.md  README.md  SCHEMA.md(generated)  kb  kb.cmd
schema/      tables.yaml (data model), views.sql (read-side views)
tools/       kb.py, ingestion scripts (indicators, Congreso)
data/        common/ (jurisdictions, topics, sources) · es/ (CSV tables, links/)
entries/es/  measures/ vote_notes/ statements/ programs/ dossiers/ history/   (Spanish)
knowledge/   <discipline>/<subfield>/kn-*.md   (English, country-agnostic)
library/     study-*.md   (one card per study)
examples/    es/*.md   (published example answers, copied from reviewed questions)
questions/   es/es-q-*.md   (questions, current answer, revision history; local, git-ignored)
build/ raw/  derived DB / original downloads (git-ignored)
```

## Adding a country

You do not need a `spain/` subfolder. Country data is already partitioned by ISO code (`data/es/`, `entries/es/`, `questions/es/`). Every id carries its country prefix (`es-…`), and `knowledge/`, `library/`, topics and sources are shared across countries. To add, say, France:

1. **Jurisdictions:** add `fr` (level `state`, parent `eu`) and its regions to `data/common/jurisdictions.csv`.
2. **Folders:** run `kb scaffold --country fr` to create the CSV files.
3. **Language:** add `"fr": "fr"` to `COUNTRY_LANG` in `tools/kb.py`.
4. **Schema:** generalise the Spain-specific details in `schema/tables.yaml`, then rebuild.
   - Widen the jurisdiction id pattern: region codes may have 1–3 characters (`FR-ARA`, `GB-ENG`) and municipality codes other lengths.
   - Add generic chamber values (e.g. `lower_house`, `upper_house`) next to `congreso` / `senado`.
5. **Ingestion:** write country-specific scripts (national statistics, parliament open data). `tools/ingest_indicators.py` and the Congreso scripts are Spain-specific. EU-wide comparison series should move to an `eu` file.
6. **Instructions:** add the country's primary sources to AGENTS.md §8.2.

## Decisions

| Topic | Decision |
|---|---|
| Names | Folders, ids, columns and enum values are English lowercase ASCII. Countries use ISO codes (`es`), regions ISO 3166-2 (`es-ct`), municipalities INE codes (`es-ct-08019`) |
| Language | Spain content is in Spanish; knowledge, instructions and tooling are in English; quotes stay in their original language; answers use the language of the question |
| Levels of government | The state level is collected fully; regional and local data is added when a question needs it |
| Time span | Context from 1977. Actions: complete for the XIV and XV legislatures (2019–), only notable ones before that |
| Parties | Those represented in the Congreso in the XV legislature, plus relevant historical ones |
| Normative stance | Positive analysis plus conditional recommendations ("if the goal is X, the evidence favours Y"); no verdicts unless asked |
| Agent autonomy | Agents write directly, mark `verification`, and humans review through git diffs |

## Contributing

Found a factual error, a missing source or a biased answer? [Open an issue](../../issues) with the entity id or the question, and what the source says. Corrections of bias are as welcome as corrections of fact.

## License

- **Code** (`tools/`, the `kb` wrappers) is licensed under [AGPL-3.0](LICENSE).
- **Data, knowledge content and documentation** are licensed under [CC BY-SA 4.0](LICENSES/CC-BY-SA-4.0.txt).
- Both licences allow commercial use with attribution, as long as derivatives are shared under the same licence.
- Third-party sources keep their own terms. [ATTRIBUTION.md](ATTRIBUTION.md) lists them, says what is this project's own elaboration, and includes a disclaimer.

## Roadmap

1. **Skeleton** ✅: data model, `kb` tool, seed registries (jurisdictions, topics, official sources, parties), AGENTS.md.
2. **Spanish context** ✅ (gaps listed in the `coverage` table):
   - central governments since 1977, legislatures, elections and seats;
   - regional and major city governments;
   - events timeline;
   - core indicators via the INE and Eurostat APIs.
3. **Knowledge for the first questions** ✅: rent regulation and housing supply; effects of immigration and of immigration policy; wealth taxation and tax-base mobility, with study cards, knowledge notes, Spanish dossiers, and related party actions and programs.
4. **Bulk ingestion** ✅: Congreso open-data votes (XIV–XV, with each deputy's vote) and initiatives (XV).
5. **First answers** ✅: seven questions answered, independently reviewed for bias and revised (four published in `examples/es/`).
6. **Next**:
   - load the 29-11-2026 general election and the new government;
   - make the independent review mandatory;
   - start a prediction log;
   - grow the knowledge base as new questions arrive.

</details>
<br/><br/>

<details>
<summary><strong><big><big>MANUAL Español</big></big></strong></summary>

## Qué es

Una base de conocimiento sobre política pensada para que un asistente de IA responda preguntas políticas de forma objetiva: con datos, razonamiento explícito y ciencia disponible, sin quedarse en el relato de los medios ni en el marketing de los partidos. **Se ha iniciado con la política española.** Puede ampliarse a otros países sin reorganizar nada.

Hoy contiene:
- **Gobiernos:** el estatal desde 1977, los autonómicos desde 2015, y los de Barcelona y Madrid desde 2011.
- **Elecciones y legislaturas.**
- **Congreso:** las 8.758 votaciones electrónicas del Pleno de 2019 a 2026, con el voto de cada diputado.
- **Cronología:** unos 260 eventos.
- **Estadísticas:** 53 series del INE y Eurostat (paro, precios, vivienda, delincuencia, sanidad, población, deuda…).
- **Temas en profundidad:** alquiler, inmigración, impuestos a las grandes fortunas, delincuencia, sanidad, e IA y leyes laborales: 142 estudios, 64 conclusiones graduadas por la fuerza de su evidencia y 47 leyes y medidas.
- **Preguntas respondidas:** siete, revisadas en busca de sesgos; cuatro están arriba como ejemplo.

## Por qué usarlo: evaluación honesta

**Ventajas frente a preguntar directamente a un chatbot**
- **Se puede comprobar todo.** Cada dato lleva su fuente, y las cifras se calculan sobre los datos, no de memoria.
- **Está al día.** Conoce hechos recientes de España que un modelo general no sabe o inventaría: la disolución de las Cortes de octubre de 2026, la regularización de 2026, los decretos de vivienda rechazados…
- **Ordena la respuesta.** Separa hechos, causas, predicciones y valores. Da efectos a corto, medio y largo plazo y por grupo afectado, con probabilidades, y dice qué falta.
- **Corrige sesgos.** Una revisión independiente encontró problemas reales en las tres primeras respuestas, por ejemplo una inclinación contra las propuestas restrictivas en la de inmigración, y se corrigieron.
- **Mejora con el uso.** Cada pregunta nueva sobre un tema ya cubierto cuesta unos minutos. Las repreguntas actualizan la misma respuesta y guardan su historial.

**Límites**
- **Base de evidencia reducida.** Hay pocos estudios españoles. Muchos datos se han verificado con fuentes secundarias, y algunos programas de partido se leyeron en copias publicadas por medios.
- **Votos de los partidos.** Las votaciones electrónicas del Congreso desde 2019 vienen de los datos abiertos oficiales; las votaciones por llamamiento, el Senado y los parlamentos autonómicos aún salen de la prensa.
- **Revisión sin humanos.** La IA que responde y la que revisa son del mismo tipo; falta una revisión humana experta.
- **Probabilidades.** Son juicios razonados, no cálculos, y aún no se ha medido si aciertan.
- **Respuestas largas.** Pide el resumen si es lo que necesitas.
- **Profundidad desigual.** Solo hay profundidad en los temas ya investigados. Un tema nuevo requiere primero una fase de investigación.

**Conclusión.** No es un oráculo ni una publicación científica revisada por expertos. Es un informe transparente y auditable: sirve para saber qué dice la evidencia, con qué seguridad y de dónde sale. Cuando no hay buena evidencia, debe decirlo.

## Cómo usarlo

0. **Instala** (Python 3.10 o superior). Descarga solo la versión actual (unos 24 MB) y prepara la base:

   ```bash
   git clone --depth 1 https://github.com/VicenteAlex/answers_for_politics.git && cd answers_for_politics
   python3 -m venv .venv && .venv/bin/python -m pip install -r requirements.txt && ./kb build
   ```

   En Windows: `python -m venv .venv`, `.\.venv\Scripts\python -m pip install -r requirements.txt` y `.\kb.cmd build`.
1. Abre un asistente con acceso a la carpeta (por ejemplo Claude Code) en este proyecto. Leerá automáticamente sus instrucciones.
2. Haz tu pregunta en lenguaje normal. El asistente consultará la base, buscará lo que falte, lo guardará con sus fuentes y responderá con el formato estándar.
3. En temas delicados, pide además *«una revisión independiente de sesgos y la versión corregida»*.
4. Repregunta o corrige con normalidad: la respuesta guardada se actualiza y conserva su historial.
5. Las respuestas quedan en `questions/es/`, solo en tu equipo: esa carpeta no se sube al repositorio. Lo que se aprende al responder (estudios, datos, leyes) sí se guarda en la base compartida. Puedes pedir *«qué respuestas han quedado desactualizadas»* cuando cambien los datos.
6. Para ampliar, pide por ejemplo *«investiga y guarda la evidencia sobre pensiones»* o *«añade Francia»*.

## Contribuir

¿Has encontrado un error, una fuente que falta o una respuesta sesgada? [Abre un issue](../../issues) con el id de la entidad o la pregunta y lo que dice la fuente. Las correcciones de sesgo son tan bienvenidas como las de datos.

## Licencia

- **Código:** [AGPL-3.0](LICENSE).
- **Datos y contenidos:** [CC BY-SA 4.0](LICENSES/CC-BY-SA-4.0.txt).
- **Uso comercial:** se permite, citando la fuente y compartiendo las obras derivadas con la misma licencia.
- **Fuentes externas** (Congreso, INE, Eurostat, BOE, Wikipedia): conservan sus propias condiciones, que se detallan en [ATTRIBUTION.md](ATTRIBUTION.md) junto con un aviso de responsabilidad.

</details>

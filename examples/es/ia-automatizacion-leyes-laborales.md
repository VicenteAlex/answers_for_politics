# ¿Pueden las leyes laborales cambiar el impacto de la automatización por IA en los trabajadores? Comparación derecha/izquierda y efectos previsibles

> **Pregunta (literal):** En el contexto de perdida de trabajo por la automatizacion de la IA en los proximos años, podrian las leyes laborales influenciar el impacto en los trabajadores? Si es asi, compara las leyes que proponen y que han aprobado los goviernos de derechas vs izquierdas y luego intenta predecir posibles efectos basados en la evidencia

Respuesta generada por un agente de IA con esta base de conocimiento y revisada por un segundo agente independiente en busca de sesgos y errores (versión 2, datos a 2026-11-26). Los ids entre corchetes enlazan a las entidades de la base (leyes, estudios, eventos); las cifras se calcularon con SQL sobre los datos.

**Aviso:** es un informe automatizado y auditable, no una verdad oficial. Si ves un error o un sesgo, abre un issue.

### 1. Respuesta corta

**Sí, pero sobre todo cambian *quién* soporta el ajuste y *a qué ritmo*, no cuánta automatización llega.** Hasta 2026 los efectos causales medidos de la IA sobre el empleo agregado son pequeños o nulos; las señales negativas (jóvenes, EE. UU.) son descriptivas.

- **PP (2012):** abarató el despido y amplió la flexibilidad interna (convenio de empresa, descuelgues, ERE/ERTE sin autorización).
- **PSOE-UP (2021):** restringió la temporalidad, creó el Mecanismo RED, reforzó el convenio sectorial, dio derechos de información sobre algoritmos y subió el SMI; no tocó la indemnización.
- **2026:** nadie propone abaratar el despido; la izquierda propone encarecerlo y el PP, formación portable.

Nadie ha aplicado recolocación específica para la IA. **Predicción condicional:** con difusión rápida, los más perjudicados serían los jóvenes que entran en ocupaciones expuestas (*probable*) y los administrativos veteranos que sean despedidos (despidos masivos *inciertos*; si ocurren, pérdidas grandes *muy probables*). Evidencia moderada sobre mecanismos, débil sobre la incidencia de la IA.

### 2. Hechos clave

**Tamaño y ritmo del desplazamiento**

- **Exposición no es destrucción de empleo:** ~40% del empleo mundial y ~60% en economías avanzadas está expuesto (27% con alta complementariedad, 33% baja; FMI, D) [[study-cazzaniga-2024-imf-genai-future-of-work](../../library/study-cazzaniga-2024-imf-genai-future-of-work.md)]; solo el 3,3% mundial en la exposición máxima [study-gmyrek-2025-ilo-genai-exposure-index].
  España: algo más del 30% en exposición media-alta o alta; desde 2022 el empleo creció en todos los grupos (D) [[study-bbva-research-2026-ia-empleo-expuesto-espana](../../library/study-bbva-research-2026-ia-empleo-expuesto-espana.md)].
- **Efectos sobre el empleo:** Dinamarca: se descartan efectos >2% sobre ingresos u horas a dos años (doc. de trabajo, B) [study-humlum-2025-llm-small-labor-market-effects].
  EE. UU.: empleo relativo de 22-25 años en las ocupaciones más expuestas un 13-19% menor según la versión (observacional, C, revisado varias veces) [[study-brynjolfsson-2025-canaries-coal-mine](../../library/study-brynjolfsson-2025-canaries-coal-mine.md)].
- **Productividad:** atención al cliente: +15% de casos por hora, más para novatos (B) [[study-brynjolfsson-2025-generative-ai-at-work](../../library/study-brynjolfsson-2025-generative-ai-at-work.md)]; agregado: como mucho +0,66% de PTF en 10 años (modelo, C) [[study-acemoglu-2025-simple-macroeconomics-ai](../../library/study-acemoglu-2025-simple-macroeconomics-ai.md)].
- **Robots:** en EE. UU., −0,2 puntos de tasa de empleo y −0,42% de salarios por robot adicional por mil trabajadores [[study-acemoglu-2020-robots-jobs-us](../../library/study-acemoglu-2020-robots-jobs-us.md)]; en Alemania, compensación en servicios con el ajuste en los jóvenes que no entraron [study-dauth-2021-adjustment-labor-markets-robots]; en la industria española, +10% de empleo neto en las empresas que adoptan [study-koch-2021-robots-firms-spain]; una revisión de 127 estudios ve predominar la compensación [study-hotte-2023-technology-jobs-systematic-review].
- **Coste de perder el empleo (EE. UU.):** ~25% de los ingresos anuales de forma persistente para desplazados con antigüedad [study-jacobson-1993-earnings-losses-displaced-workers]; 1,4 años de salario con paro <6% y 2,8 con paro >8% [study-davis-2011-recessions-costs-job-loss].

**Contexto en España** (Eurostat, EPA)

| Asalariados temporales | 2011 | 2013 | 2018 | 2021 | 2025 | UE-27 (2025) |
|---|---|---|---|---|---|---|
| 15-64 años | 25,2% | 23,2% | 26,9% | 25,4% | 15,4% | 12,6% |
| 15-24 años | 61,2% | 64,7% | 71,2% | 69,1% | 44,4% | 47,2% |

[es-temporary-employees-share; es-temporary-employees-share-15-24]. Tras 2012 la temporalidad subió con la recuperación; tras 2021 cayó unos 10 puntos (descriptivo).

Paro (T3 2026): 10,18%; menores de 25: 23,33% [es-unemployment-rate; es-youth-unemployment-rate]. Adultos en formación: 15,8% en 2025 (UE-27: 13,7%; ruptura de serie en 2021) [es-adult-learning-participation].

**Qué aprobó cada bloque** (BOE; votos de `v_vote_party`)

| Gobierno | Norma | Contenido relevante | Apoyos |
|---|---|---|---|
| PP | RDL 3/2012 y Ley 3/2012 [[es-measure-rdl-3-2012-reforma-laboral](../../entries/es/measures/es-measure-rdl-3-2012-reforma-laboral.md)] | Improcedente de 45 a 33 días/año (tope 42→24 mensualidades); causas económicas definidas; ERE/ERTE sin autorización; prioridad del convenio de empresa | 197-142 (08/03/2012): PP, CiU, UPN, Foro; en contra PSOE, IU y otros (Diario de Sesiones) |
| PSOE-UP | RDL 9/2021, ley rider [[es-measure-rdl-9-2021-ley-rider](../../entries/es/measures/es-measure-rdl-9-2021-ley-rider.md)] | Art. 64.4.d ET: el comité conoce los parámetros de los algoritmos que afectan al empleo | 195-151; en contra PP, Vox, Cs, UPN, Foro [es-vote-xiv-2021-06-10-s106-v012] |
| PSOE-UP (pactado con CEOE, Cepyme, CCOO, UGT) | RDL 32/2021 [[es-measure-rdl-32-2021-reforma-laboral](../../entries/es/measures/es-measure-rdl-32-2021-reforma-laboral.md)] | Contrato indefinido por defecto; fin de obra y servicio; más fijo discontinuo; ERTE y Mecanismo RED (el sectorial exige plan de recualificación); convenio sectorial en salarios. **No cambia la indemnización** | 175-174: PSOE, UP, Cs, PDeCAT y regionalistas; en contra PP (un voto a favor por error), Vox, ERC, PNV, Junts, Bildu, BNG, CUP, UPN [es-vote-xiv-2022-02-03-s149-v020] |
| PSOE-UP | Ley 3/2023 de Empleo [[es-measure-ley-3-2023-empleo](../../entries/es/measures/es-measure-ley-3-2023-empleo.md)] | Políticas activas en las CC. AA.; "sectores en reestructuración" como colectivo prioritario; la Agencia de Empleo no constaba creada en sept. 2026 | 187-58-101; abstención PP, Cs, Junts; en contra Vox, BNG, CUP [es-vote-xiv-2022-12-22-s229-v370] |
| PSOE-UP / PSOE-Sumar | SMI [[es-measure-smi-2018-2027](../../entries/es/measures/es-measure-smi-2018-2027.md)] | 735,90 € (2018) → 1.221 € (2026): +65,9% nominal, ~+31% real (IPC medio anual; 2026 hasta octubre) | Real decreto |
| PSOE | RD 729/2023 [[es-measure-rd-729-2023-estatuto-aesia](../../entries/es/measures/es-measure-rd-729-2023-estatuto-aesia.md)] | AESIA (también prometida por el PP en 2023) | — |

**Nivel UE** (no atribuible a un bloque español): el Reglamento de IA considera de alto riesgo la IA de contratación y gestión de personal; la obligación de informar a los representantes (art. 26.7) se aplica desde el **02/12/2027** tras el ómnibus 2026/1744 [[eu-measure-reglamento-2024-1689-ley-ia](../../entries/global/measures/eu-measure-reglamento-2024-1689-ley-ia.md)]. La Directiva 2024/2831 de plataformas debe transponerse antes del 02/12/2026 y no consta norma española [[eu-measure-directiva-2024-2831-trabajo-plataformas](../../entries/global/measures/eu-measure-directiva-2024-2831-trabajo-plataformas.md)].

**No salieron adelante:** la ley de 37,5 h, devuelta el 10/09/2025 por 178-170 (PP, Vox, Junts, UPN) [es-vote-xv-2025-09-10-s130-v010]; la proposición de 35 h, rechazada por 162-178 (en contra PP, Vox, Junts, UPN; abstención del PNV) [es-vote-xv-2025-10-14-s137-v001]; y la ley orgánica de IA, que caducó con la disolución [es-event-2026-05-26-proyecto-ley-ia].

**Evaluaciones de las reformas** (grado D, sin grupo de control)

- **2012:** moderación salarial (subidas pactadas del 1,3% en 2012), flexibilidad interna sobre todo en grandes empresas, "cierto impacto positivo en el empleo neto" ("menos concluyente") y sin cambio en la dualidad [study-izquierdo-2013-reforma-laboral-2012-primer-analisis].
- **2021:** el paso de temporal a indefinido en un año subió del 18% al 33% [[study-conde-ruiz-2025-reforma-laboral-2021-temporalidad](../../library/study-conde-ruiz-2025-reforma-laboral-2021-temporalidad.md)], pero la duración mediana de los periodos de fijo discontinuo bajó de 84 a 8 días [study-hernanz-2026-fijo-discontinuo-genero].

### 3. Mecanismos (causales; grado entre paréntesis)

- **Despido caro → menos despidos de fijos, pero menos contratación y menos experimentación tecnológica → el ajuste recae en quienes entran** (B-C, entre países) [[study-bartelsman-2016-employment-protection-technology-choice](../../library/study-bartelsman-2016-employment-protection-technology-choice.md); [study-bassanini-2009-job-protection-productivity-oecd](../../library/study-bassanini-2009-job-protection-productivity-oecd.md); [study-autor-2007-wrongful-discharge-productivity](../../library/study-autor-2007-wrongful-discharge-productivity.md)]. En España, abaratarlo en 2012 no redujo la dualidad (D).
- **Despido barato → reasignación más rápida y más despidos de veteranos**, con pérdidas grandes y persistentes (B) [study-jacobson-1993-earnings-losses-displaced-workers].
- **Flexibilidad interna → ajuste sin despidos** ante shocks de empresa: canal principal de 2012 (D) y de los ERTE.
- **ERTE / RED → conservan empleo ante shocks temporales; frenan la reasignación ante shocks persistentes** (B) [study-giupponi-2023-short-time-work-italy; study-giupponi-2022-insure-workers-or-jobs; [study-cahuc-2021-short-time-work-france](../../library/study-cahuc-2021-short-time-work-france.md)]. ERTE COVID: reincorporación del 65% al 26% según duración, aún 13 puntos sobre parados comparables (C) [study-izquierdo-2022-erte-efectividad-duracion]. *Supuesto:* si la IA es un shock estructural, lo pertinente es el RED sectorial.
- **Formación → efectos pequeños a corto plazo y positivos a 2-3 años; el diseño importa** (A) [[study-card-2018-almp-meta-analysis](../../library/study-card-2018-almp-meta-analysis.md); study-kluve-2010-european-almp-meta-analysis].
- **Prestación más larga → algo más de paro (0,1 meses por mes extra), sin peores empleos** (B) [study-schmieder-2012-extended-ui-business-cycle; study-nekoei-2017-ui-extension-job-quality].
- **SMI alto → menos empleo en tareas automatizables poco cualificadas** (B, EE. UU.) [study-lordan-2018-minimum-wages-automatable-jobs]. SMI 2019 en España: +1,7 puntos de probabilidad de pasar al paro de los afectados (B) [study-gorjon-2023-minimum-wage-spain-2019] o −6 a −11 puntos de su empleo neto (C, sin revisión por pares) [[study-barcelo-2021-smi-2019-empleo](../../library/study-barcelo-2021-smi-2019-empleo.md)]; métricas distintas. Canal menos relevante para la IA generativa, que expone tareas cognitivas mejor pagadas.
- **Sindicatos → protegen a los de dentro; pérdidas para jóvenes y poco formados** (C) [study-haapanala-2023-robots-unions; study-parolin-2021-automation-organized-labor; [study-belloc-2022-automation-risk-workplace-governance](../../library/study-belloc-2022-automation-risk-workplace-governance.md)]. Los derechos sobre algoritmos no se han evaluado.
- **Reducción legal de jornada → sin empleo neto en Francia** (B) [study-crepon-2002-employed-40-hours; [study-chemin-2009-35-hour-alsace-moselle](../../library/study-chemin-2009-35-hour-alsace-moselle.md)]; en Portugal, más salario por hora y menos separaciones [study-raposo-2010-working-time-reduction-portugal].
- **Impuesto a la automatización → solo uno pequeño y temporal, o neutralizar sesgos pro-capital** (teoría, C) [study-guerreiro-2022-should-robots-be-taxed; [study-acemoglu-2020-us-tax-code-automation](../../library/study-acemoglu-2020-us-tax-code-automation.md)].

### 4. Efectos previstos (predicción; muy incierta)

Escenarios: **lento** (ritmo de 2023-2026) y **rápido** (sustitución generalizada de tareas administrativas, de atención al cliente y de programación desde 2027). El rápido en 5 años es *incierto* (40-60%); las probabilidades son condicionales a cada escenario.

| Grupo | <1 año | 1-5 años | >5 años | Evidencia |
|---|---|---|---|---|
| Jóvenes que entran en ocupaciones expuestas | Lento: improbable que se note. Rápido: menos contratación, probable | Lento: incierto. Rápido: caída relativa muy probable | Recuperación parcial: incierta | Moderada (robots) / débil (IA) |
| Administrativos con antigüedad | Recolocación interna (probable) | Despidos masivos: lento improbable, rápido incierto. Si ocurren, pérdidas del 20-25% persistentes: muy probable | Según recualificación | Fuerte (coste) / débil (incidencia) |
| Poco cualificados, tareas manuales | Poco afectados por la IA generativa | Automatización clásica, algo mayor con SMI alto: probable, pequeña | Incierto | Moderada |
| Mayores de 55 | Protegidos | Si se les despide, reempleo difícil: muy probable | — | Moderada |
| Empresas | Ganancias en tareas concretas: casi seguro | Protección estricta frena la reorganización: probable, pequeño | PTF modesta (<1% en 10 años) | Moderada |
| Presupuesto | Sin efecto apreciable | Rápido: más gasto en desempleo, RED y formación: probable | Incierto | Débil |

**Efecto de cada opción legal (escenario rápido):**

- **Abaratar el despido** (nadie lo propone en 2026): más reasignación (probable); más contratación indefinida de jóvenes (incierto: no ocurrió tras 2012); más pérdidas de veteranos (muy probable).
- **Encarecer el despido o exigir autorización previa** (PSOE, Frente Amplio): menos despidos de fijos (probable); más ajuste vía no contratación de jóvenes y adopción algo más lenta (probable, efecto pequeño-moderado).
- **Cotización por despidos debidos a la IA** (Frente Amplio): sin evaluar; causa difícil de atribuir; desplazaría el ajuste a la no contratación (incierto).
- **Formación portable** (PP) o **RED sectorial** (PSOE-UP): mejor encaje con la evidencia si el diseño es bueno; sin evaluar.

### 5. Dónde discrepa la evidencia

- **¿La IA ya destruye empleo?** Nulo en Dinamarca, caída juvenil en EE. UU. Crux: IA frente a tipos y ciclo tecnológico.
- **Robots:** pérdidas en EE. UU., compensación en Alemania y España. Crux: demanda e instituciones, y si la IA se comportará igual.
- **Protección del empleo:** entre países frena la reasignación; en España la dualidad respondió más a las reglas sobre temporales que a la indemnización (descriptivo).
- **SMI 2019:** de pequeños a moderados según método y grupo de control.

### 6. Qué depende de valores

Asegurar *puestos* (protección, ERTE) o *personas* (prestación, formación, movilidad); proteger a quien trabaja o a quien entra.

- **Si el objetivo es minimizar las pérdidas de quien ya trabaja**, la evidencia favorece protección y ERTE, al coste de menos contratación juvenil y adopción más lenta.
- **Si el objetivo es la reasignación y la entrada de jóvenes**, favorece despido menos costoso con seguro y formación generosos (flexiseguridad), de alto coste fiscal y evidencia sobre todo descriptiva (D) [[study-andersen-2007-flexicurity-denmark](../../library/study-andersen-2007-flexicurity-denmark.md)].

**Argumentos más fuertes, en sus propios términos:**

- **Derecha:** quien adopta tecnología crea empleo y la flexibilidad facilita adoptar; la flexibilidad interna de 2012 ajustó salarios y horas en vez de despedir; un despido caro protege a los de dentro a costa de los que entran; un SMI alto acelera la automatización poco cualificada; la formación portable sigue a la persona.
- **Izquierda:** perder el empleo cuesta mucho y durante años; la temporalidad juvenil cayó tras 2021 y no tras 2012; ERTE y RED conservan capital humano; el poder de negociación decide quién se queda las ganancias de productividad; la gestión algorítmica exige información y revisión humana.

### 7. Partidos: hechos frente a palabras

| Partido | Hechos | 2023 | 2026 |
|---|---|---|---|
| PP | Reforma de 2012; en contra de ley rider y reforma de 2021; abstención en Ley de Empleo y (dividido) en la PNL de IA de 2024 [es-vote-xv-2024-06-13-s046-v016] | Cuentas individuales portables, reforma de políticas activas, agencia de IA [[es-program-2023-pp](../../entries/es/programs/es-program-2023-pp.md)] | Cheque de formación portable (apartado de IA), menos cotización por desempleo con plantillas estables, bolsas de horas; nada sobre indemnización [[es-program-2026-pp](../../entries/es/programs/es-program-2026-pp.md)] |
| Vox | En contra de reforma de 2021, ley rider y Ley de Empleo | Derogar "la reforma laboral de Yolanda Díaz" [[es-program-2023-vox](../../entries/es/programs/es-program-2023-vox.md)] | "Derogar la legislación laboral de Sánchez", sin sustituto; IA como promoción [[es-program-2026-vox](../../entries/es/programs/es-program-2026-vox.md)] |
| PSOE | Reforma de 2021, ley rider, Ley de Empleo, SMI, AESIA; jornada e IA fallidas | SMI al 60% por ley (incumplido); acompañamiento ante la IA [[es-program-2023-psoe](../../entries/es/programs/es-program-2023-psoe.md)] | 37,5 h y 35 h por convenio; despido "disuasorio" y salarios de tramitación; transparencia algorítmica; impuestos a tecnológicas [[es-program-2026-psoe](../../entries/es/programs/es-program-2026-psoe.md)] |
| Sumar / Frente Amplio | Socio de gobierno desde 2020 | 37,5 h por ley en 2024 (incumplido); auditoría algorítmica [[es-program-2023-sumar](../../entries/es/programs/es-program-2023-sumar.md)] | 37,5 h y luego 32 h; autorización previa de ERE; cotización por despidos debidos a la IA; prestación del 80%; impuesto europeo del 50% en acciones a grandes empresas de IA [[es-program-2026-frente-amplio](../../entries/es/programs/es-program-2026-frente-amplio.md)] |

**Test de simetría:**

- Ambos bloques votaron contra la reforma del otro; la de 2021 fue pactada con patronal y sindicatos, la de 2012 no.
- La línea no es limpia: Cs apoyó la reforma de 2021 y ERC, PNV, Bildu, BNG y CUP la rechazaron; Junts votó con PP y Vox sobre la jornada.
- La izquierda tuvo una ley de IA que caducó; la derecha propone formación, no regulación laboral de la IA.

### 8. Qué cambiaría la conclusión

Evidencia causal de caída del empleo juvenil en ocupaciones expuestas en España; evaluaciones del RED, del art. 64.4.d ET o de la cotización por despido por IA; un salto medido de la productividad agregada.

### 9. Limitaciones

- Evidencia sobre la IA: 2023-2026, sobre todo EE. UU. y Dinamarca; varios estudios clave son documentos de trabajo. Las reformas españolas solo tienen evaluaciones descriptivas en la KB.
- Faltan medidas autonómicas, aunque las CC. AA. (de ambos bloques) ejecutan las políticas activas; las medidas laborales son una muestra (`es-cov-measures-labor-central`).
- Sin votos nominales anteriores a diciembre de 2019 (los de 2012 vienen del Diario de Sesiones). El programa de Vox de 2026 solo está verificado con fuentes secundarias.

### 10. Fuentes

Ids de la KB en el texto (URL en cada ficha). Eurostat (lfsa_etpgan, trng_lfse_01), INE (EPA, IPC), BOE y DOUE, consultados el 2026-11-26.

## Historial de revisiones

- v1 · 2026-11-26 · Primera respuesta. Se han creado unas 47 fichas de estudios, la nota kn-automation-ai-labor-institutions, 8 medidas, 3 eventos, 8 programas con 49 promesas y 3 series de Eurostat · nueva evidencia.
- v2 · 2026-11-26 · revisión independiente de sesgos · Simetría 2012/2021: se añaden la evaluación del Banco de España de la reforma de 2012 y la trayectoria de la temporalidad tras 2012 y tras 2021; se describe la flexibilidad interna de 2012 y el refuerzo del convenio sectorial en 2021; las transiciones de temporal a indefinido (+) junto al fijo discontinuo (−); la ventaja de los ERTE frente a parados comparables. Correcciones: listas de votos completas (RDL 32/2021, ley rider, Ley de Empleo, 35 h); el PSOE 2026 propone 35 h por convenio, no por ley; Raposo (Portugal) no mide empleo neto; métricas del SMI 2019 separadas; SMI deflactado (+31% real 2018-2026); art. 26.7 del Reglamento de IA aplicable desde 02/12/2027. Se elimina una afirmación sin fuente («trabajo no publicado sin efecto del SMI»), el riesgo de deslocalización sin evidencia y la cifra del 34% para novatos. Predicciones del resumen condicionadas al escenario y recalibradas; se señala que ningún programa de 2026 propone abaratar el despido y que la línea derecha-izquierda no es limpia (Cs, ERC/PNV/Bildu, Junts). Se añade la cobertura es-cov-measures-labor-central y se marca la ausencia de medidas autonómicas. Respuesta de ~2.760 a ~2.300 palabras · corrección.

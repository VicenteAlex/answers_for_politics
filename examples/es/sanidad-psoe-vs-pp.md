# Legislación sanitaria del último Gobierno del PSOE frente al último del PP, y acceso a la sanidad

> **Pregunta (literal):** Que legislaciones han llevado a cabo el ultimo govierno del PSOE vs el ultimo govierno del PP en materia de salud. El acceso a servicios de salud de la poblacion con quien ha sido mejor?

Respuesta generada por un agente de IA con esta base de conocimiento y revisada por un segundo agente independiente en busca de sesgos y errores (versión 2, datos a 2026-11-26). Los ids entre corchetes enlazan a las entidades de la base (leyes, estudios, eventos); las cifras se calcularon con SQL sobre los datos.

**Aviso:** es un informe automatizado y auditable, no una verdad oficial. Si ves un error o un sesgo, abre un issue.

### 1. Respuesta corta
- **Legislación (hecho, BOE).** El Gobierno Rajoy (PP, dic. 2011-jun. 2018) **restringió** el derecho y la gratuidad: condición de "asegurado" (inmigrantes adultos sin papeles limitados a urgencias, embarazo y parto), copago para pensionistas y recortes de personal y gasto, en plena crisis de deuda; también financió los antivirales de la hepatitis C (2015). El Gobierno Sánchez (PSOE y coaliciones, jun. 2018-2026) **amplió**: acceso universal, exenciones de copago, cartera dental, eutanasia y Agencia de Salud Pública.
- **Acceso.** No hay un ganador limpio; depende del indicador:
  - *Derecho legal a la asistencia*: más amplio con el PSOE (casi seguro, es un hecho normativo).
  - *Barreras por coste*: máximas en 2011-2014 (crisis y copago), pero ya bajas en 2015-2018, aún con el PP. Fuera de la crisis, la diferencia es pequeña.
  - *Esperas*: niveles más altos con el PSOE, y la necesidad no cubierta por espera se multiplicó desde 2020 (probable que el acceso efectivo fuera peor en 2020-2025). Pero en ventanas sin rotura de serie ambos periodos empeoran en algún indicador, y las listas son autonómicas: la atribución al Gobierno central es débil.

### 2. Reparto de competencias y quién gobernaba las CCAA
Las 17 CCAA gestionan la asistencia (plantillas, listas, la mayor parte del gasto); el Estado fija derecho, cartera común, medicamentos, copago y salud pública. Se comparan solo **normas estatales**; los indicadores nacionales no se atribuyen al Gobierno central salvo con estudios causales (exclusión de 2012, copagos).

Color de los gobiernos autonómicos (KB, `v_governments`):
- **2012-2015:** PP en unas 11 CCAA (recortes del PP en ambos niveles).
- **2015-2019:** mayoría PSOE o coaliciones de izquierda.
- **2019-2023:** PP en Andalucía, Castilla y León, Galicia, Madrid y Murcia (más del 40% de la población).
- **Desde mediados de 2023:** el PP preside 11 CCAA y co-gobierna Canarias. Las esperas de 2023-2025 corresponden sobre todo a servicios de salud del PP.

### 3. Hechos clave: legislación estatal

**Rajoy (PP)**
- **RDL 16/2012** (convalidado 17/05/2012) [[es-measure-rdl-16-2012-sostenibilidad-sns](../../entries/es/measures/es-measure-rdl-16-2012-sostenibilidad-sns.md)]:
  - Condición de "asegurado" (menores siguieron cubiertos); cartera común dividida en básica, suplementaria y accesoria.
  - Copago farmacéutico por renta: pensionistas, del 0% al 10% con topes de 8 o 18 €/mes (60% sin tope por encima de 100.000 €); activos, 40/50/60%. Exentos: parados sin prestación, rentas mínimas, pensiones no contributivas.
- **Desarrollo:** RD 1192/2012 (asegurado) y RD 576/2013 (convenio especial de 60 €/mes, 157 € desde 65 años) [[es-measure-rd-1192-2012-condicion-asegurado](../../entries/es/measures/es-measure-rd-1192-2012-condicion-asegurado.md)]; desfinanciación de 417 presentaciones de medicamentos (Resolución 2/8/2012) [[es-measure-res-2012-08-02-exclusion-medicamentos](../../entries/es/measures/es-measure-res-2012-08-02-exclusion-medicamentos.md)].
- **Personal (Ley 2/2012 de PGE y RDL 20/2012):** tasa de reposición del 10%, jornada de 37,5 h y supresión de la paga extra de diciembre de 2012 [[es-measure-ley-2-2012-pge-personal-sanitario](../../entries/es/measures/es-measure-ley-2-2012-pge-personal-sanitario.md)].
- **Hepatitis C (2015, plan del Consejo Interterritorial, no ley):** antivirales de acción directa garantizados para fibrosis F2-F4; 59.948 pacientes tratados hasta sept. 2016, según Sanidad [es-event-2015-03-26-plan-estrategico-hepatitis-c].
- **Tribunal Constitucional:** la STC 139/2016 avaló el modelo de asegurado salvo un inciso [es-event-2016-07-21-stc-139-2016-rdl-16-2012]. A recurso del Gobierno, el TC anuló las normas de País Vasco, C. Valenciana y Navarra que mantenían la atención a los excluidos (STC 134/2017, 145/2017, 17/2018 y 18/2018) [es-event-2017-12-14-stc-145-2017-acceso-universal-valencia].
- **Otras, de menor impacto en el acceso:** Ley 10/2013 (farmacovigilancia), RDLeg 1/2015 (medicamento), RD 954/2015 (prescripción enfermera).

**Sánchez (PSOE; PSOE-UP/Sumar)**
- **RDL 7/2018, acceso universal:** extranjeros sin residencia legal atendidos en las mismas condiciones que los españoles, con requisitos. Convalidado 177-133 (PP en contra)-31 [[es-measure-rdl-7-2018-acceso-universal-sns](../../entries/es/measures/es-measure-rdl-7-2018-acceso-universal-sns.md)].
- **Copago farmacéutico:**
  - Ley 11/2020 (PGE 2021): exentos perceptores del IMV, menores con discapacidad, prestación por hijo a cargo y pensionistas con base liquidable < 5.635 € (u 11.200 € sin obligación de declarar) [[es-measure-ley-11-2020-pge-2021-exencion-copago](../../entries/es/measures/es-measure-ley-11-2020-pge-2021-exencion-copago.md)].
  - RDL 11/2026: más tramos y topes, exención de pensionistas con complementos a mínimos; convalidado 164-33 (Vox)-149 (PP, ERC, Junts) [[es-measure-rdl-11-2026-copago-farmaceutico](../../entries/es/measures/es-measure-rdl-11-2026-copago-farmaceutico.md)]. La estructura de 2012 para activos se mantuvo hasta 2026.
- **Eutanasia (LO 3/2021):** 202-141 (PP, Vox, UPN, Foro); recursos de Vox y PP desestimados (STC 19/2023 y 94/2023) [[es-measure-lo-3-2021-eutanasia](../../entries/es/measures/es-measure-lo-3-2021-eutanasia.md)].
- **LO 1/2023 de salud sexual y reproductiva:** aborto garantizado en centros públicos, anticonceptivos gratuitos; 185-154 [[es-measure-lo-1-2023-salud-sexual-reproductiva](../../entries/es/measures/es-measure-lo-1-2023-salud-sexual-reproductiva.md)].
- **Salud bucodental (Orden SND/606/2024):** cartera infantil (0-14), embarazadas, discapacidad y pacientes oncológicos [[es-measure-orden-snd-606-2024-salud-bucodental](../../entries/es/measures/es-measure-orden-snd-606-2024-salud-bucodental.md)].
- **Ley 3/2024 ELA:** 344-0; nació de proposiciones de Junts, PP y PSOE [[es-measure-ley-3-2024-ela](../../entries/es/measures/es-measure-ley-3-2024-ela.md)].
- **Ley 7/2025, Agencia Estatal de Salud Pública:** un primer proyecto cayó (167-176: PP, Vox y Junts); el segundo se aprobó en julio de 2025 [[es-measure-ley-7-2025-agencia-salud-publica](../../entries/es/measures/es-measure-ley-7-2025-agencia-salud-publica.md)].
- **COVID-19:** Ley 2/2021 (del RDL 21/2020, convalidado con el voto a favor del PP) [[es-measure-ley-2-2021-covid-medidas-urgentes](../../entries/es/measures/es-measure-ley-2-2021-covid-medidas-urgentes.md)].
- **Personal:** RDL 12/2022 sobre temporalidad del personal estatutario, 270-0 [[es-measure-rdl-12-2022-temporalidad-estatuto-marco](../../entries/es/measures/es-measure-rdl-12-2022-temporalidad-estatuto-marco.md)].
- **No aprobadas:** la ley de equidad, universalidad y cohesión del SNS; la nueva ley del medicamento y la reforma antitabaco decayeron con la disolución de las Cortes (BOCG, sept. 2026).

### 4. Hechos clave: acceso (datos)
Eurostat (EU-SILC; año de encuesta) y Ministerio de Sanidad.

| Indicador | 2011 | 2013-14 | 2017-18 | 2019 | 2021 | 2024-25 |
|---|---|---|---|---|---|---|
| Necesidad médica no cubierta (coste, distancia o espera), % 16+ | 0,6 | 0,8 / 0,6 | 0,1 / 0,2 | 0,2 | 1,1 | 1,8 / 1,6 |
| … quintil más pobre | 1,0 | 1,4 / 1,8 | 0,2 / 0,2 | 0,1 | 1,0 | 1,6 / 1,6 |
| … por lista de espera | 0,1 | 0,1 / 0,1 | 0,1 / 0,1 | 0,2 | 1,0 | 1,6 / 1,5 |
| … por coste | 0,4 | 0,6 / 0,5 | 0,0 / 0,1 | 0,0 | 0,1 | 0,1 / 0,2 |
| Gasto sanitario público real por habitante, € de 2015 | 1.573 | 1.415 / 1.421 | 1.549 / 1.578 | 1.631 | 1.828 | 1.779 (2024) |
| Pago directo de los hogares, % del gasto sanitario | 21,7 | 24,2 / 24,7 | 24,1 / 24,2 | 23,9 | 21,3 | 21,5 (2024) |
| Enfermeras en ejercicio por 100.000 hab. | 522 | 514 / 515 | 574 / 585 | 588 | 628 | 573 (2024) |
| Médicos en ejercicio por 100.000 hab. | 384 | 381 / 380 | 388 / 402 | 441 | 449 | 464 (2024) |

Fuentes: [es-health-unmet-medical-access-total], [es-health-unmet-medical-access-q1], [es-health-unmet-medical-waiting-total], [es-health-unmet-medical-cost-total], [es-health-exp-public-per-capita-real], [es-health-exp-out-of-pocket-share], [es-nurses-per-100k], [es-physicians-per-100k].

- **Comparación UE.** La necesidad no cubierta en España sigue por debajo de la UE-27 (2,4% en 2025). La debida a esperas también subió en la UE (0,6% en 2018 → 1,2% en 2025), pero menos que en España (0,1% → 1,5%). Gasto público sanitario: 6,68% del PIB en España frente a 8,17% en la UE-27 (2024) [es-health-exp-public-pct-gdp].
- **Gasto real por habitante.** Con el PP, −10,1% en 2011-2013 y vuelta al nivel de 2011 en 2018 (+0,3%); la caída empezó con Zapatero (−5,9% en 2009-2011). Con el PSOE subió un 12,7% entre 2018 y 2024 (UE-27: +13,2%), con el pico en 2021 por la COVID-19. En % del PIB: 6,71 → 6,28 (2011-2018) y 6,28 → 6,68 (2018-2024).
- **Plantillas (público y privado).** Las enfermeras crecieron un 12% en 2011-2018 y bajaron un 9% desde el máximo de 2021 hasta 2024. Los médicos subieron un 5% en 2011-2018 y un 15% en 2018-2024; el salto de 2019 (+9,5% en un año) puede reflejar un cambio de registro (no verificado).
- **Listas de espera quirúrgica (SISLE, diciembre salvo indicación)** [study-sanidad-2026-sisle-listas-espera-2011-2025]. La serie tiene roturas en jun. 2012 (entra Madrid), dic. 2016 (Cataluña completa) y dic. 2018 (cambio de cómputo en Andalucía, de 73 a 214 días). Comparando solo dentro de ventanas sin rotura:

| Ventana | Días de espera media | Pacientes por 1.000 | % > 6 meses |
|---|---|---|---|
| PP, jun. 2012 → dic. 2015 | 76 → 89 (+17%) | 11,8 → 12,2 | 9,4 → 10,6 |
| PSOE, dic. 2018 → dic. 2025 | 129 → 122 (−5%) | 14,8 → 17,7 (+20%) | 20,0 → 21,6 |

  - Primera consulta de especialista: 53 días (jun. 2012) → 58 (dic. 2015); 96 (dic. 2018) → 102 (dic. 2025), con 62,5 → 84,4 pacientes por 1.000.
  - Los niveles, más altos con el PSOE, reflejan en parte la rotura de 2018, el envejecimiento y la población con tarjeta (45,4 → 48,3 millones, 2019-2025).
- **Opinión** [study-sanidad-cis-2025-barometro-sanitario]: satisfacción 6,59 (2011) → 6,31 (2014) → 6,74 (2019) → 6,02 (2025), con cambio a encuesta telefónica en 2022; seguro privado propio 13,7% (2018) → 20,4% (2025).

### 5. Mecanismos y evidencia causal
- **Exclusión de 2012.** Menos atención programada → tratamiento más tardío → más mortalidad evitable.
  - DiD: +16,7% de mortalidad del grupo en tres años, +34,3% en causas tratables, ~82 muertes/año (cota inferior); placebo nulo (B) [study-juanmarti-2021-deadly-effects-losing-health-insurance].
  - Cayó la atención programada sin que las urgencias la compensaran (B) [study-jimenez-rubio-2020-limiting-access-undocumented].
  - Varias CCAA mantuvieron la cobertura; las 873.000 son tarjetas dadas de baja, no personas sin atención [study-peralta-gallego-2018-undocumented-exclusion-spain].
- **Copago de 2012.** Un precio por receta reduce el consumo, también de fármacos eficaces, más en rentas bajas.
  - Las dispensaciones cayeron más de un 10% en 15 de 17 CCAA (C) [study-puig-junoy-2014-paying-formerly-free-medicines].
  - Tras síndrome coronario agudo, adherencia de pensionistas −6,8% (IECA/ARA-II) y −8,3% (estatinas), transitoria; nula en fármacos baratos (B) [study-gonzalez-lopez-valcarcel-2017-cost-sharing-acs-adherence].
  - Esquizofrenia: adherencia OR 0,70 y hospitalizaciones OR 1,13 (B) [study-serra-burriel-2021-cost-sharing-schizophrenia].
  - La no adherencia inicial creció sobre todo en rentas bajas (C) [[study-aznar-lou-2018-copayment-initial-non-adherence](../../library/study-aznar-lou-2018-copayment-initial-non-adherence.md)].
- **Exenciones de 2021 y 2026.** Sin evaluar. Análogo: la gratuidad valenciana de 2016 para pensionistas de renta baja subió las recetas un 6-7%, con coste mayor que la recaudación perdida y salud sin medir (B) [study-puig-junoy-2020-free-prescriptions-low-income-pensioners].
- **Esperas.** Crecen si la demanda (envejecimiento, población, COVID-19) supera la capacidad (plantillas, gestión autonómica). Ningún estudio causal las atribuye a un gobierno central.
- **Ciclo.** La mortalidad cayó más deprisa en la recesión de 2008-2011: los resultados agregados de salud no sirven para juzgar la política sanitaria [study-regidor-2016-mortality-crisis-spain].

### 6. Efectos por grupo (normas estatales)

| Grupo | Rajoy | Sánchez | Evidencia |
|---|---|---|---|
| Inmigrantes sin residencia legal | Pierden la atención no urgente; más mortalidad evitable (muy probable) | Recuperan el derecho; aplicación desigual al principio [study-reder-2018-no-dejar-a-nadie-atras] | Moderada (B) / débil (D) |
| Pensionistas de renta baja | Pasan a pagar el 10% (tope de 8 €/mes); adherencia menor, temporal | Exentos desde 2021 (renta) y 2026 (mínimos); más consumo y más coste | Moderada |
| Pensionistas de renta alta | Pasan de 0% a 10-60% | Sin cambio relevante | Descriptiva |
| Pacientes de hepatitis C | Acceso a antivirales desde 2015 | Continuidad | Descriptiva |
| Población general: esperas | Suben en 2012-2013 y bajan en 2014-2015 | Suben los pacientes en lista; los días se estabilizan desde 2021 | Atribución débil (autonómica) |
| Presupuesto público | Ahorro por copago y exclusión; gasto real a la baja | Más gasto (exenciones, cartera, COVID-19) | Descriptiva |

La necesidad dental no cubierta del quintil más pobre (7,4% en 2011, 17,5% en 2014, 8,7% en 2025) sigue sobre todo a la renta: la dental de adultos estaba fuera de la cartera en ambos periodos.

### 7. Argumentos de cada parte (steelman)
- **PP.**
  - Con déficit muy alto, prima de riesgo disparada y rescate bancario, recortar era condición de solvencia; el gasto ya caía desde 2010 (RDL 8/2010 de Zapatero recortó salarios públicos).
  - Antes de 2012 todo pensionista tenía fármacos gratis fuera cual fuera su renta; el copago introdujo progresividad, topes y exenciones.
  - El aseguramiento alineaba el derecho con la residencia legal (Directiva 2004/38) y limitaba el uso por no residentes. Financió la hepatitis C a gran escala.
- **PSOE.**
  - La universalidad evita muertes (evidencia B); las exenciones protegen a quien más dejaba la medicación.
  - Amplió cartera, salud pública y derechos, y afrontó la COVID-19 con gasto récord.
  - El deterioro de las esperas es autonómico y pospandémico, también en la UE.
- **Prueba de simetría.** La mejora de las esperas en 2014-2015 (PP) y su empeoramiento en 2019-2023 (PSOE) se juzgan igual: ninguno prueba gestión central. El gasto bajó con un rescate y subió con una pandemia: ninguna cifra mide sola la "prioridad" de cada partido.

### 8. Donde la evidencia no coincide
- **Copago y salud.** Reduce el volumen (consenso); el daño depende del fármaco y del paciente, y parte de la caída puede ser desperdicio evitado.
- **Esperas desde 2018.** Gestión autonómica, plantillas, COVID-19 o demanda: los datos no las separan. El salto de la EU-SILC coincide con su cambio de marco en 2021 (posible rotura, no verificada).

### 9. Qué depende de valores
- **Universalidad frente a sostenibilidad y uso por no residentes.** Si el objetivo es minimizar la mortalidad evitable, la evidencia favorece la cobertura universal, a costa de más gasto.
- **Copago.** Si el objetivo es contener el gasto farmacéutico, el copago funciona, a costa de cierta pérdida de adherencia en grupos vulnerables; los topes bajos y las exenciones por renta reducen ese coste.
- **Eutanasia y aborto.** Son cuestiones de valores, no de acceso medible.

### 10. Partidos: hechos frente a discurso
- **PP.** Votó contra el RDL 7/2018, la eutanasia y la LO 1/2023, y recurrió la de eutanasia (la LO 1/2023 la recurrió Vox). Se abstuvo en el RDL 11/2026; apoyó la Ley ELA, el RDL 12/2022 y las medidas COVID de junio de 2020.
- **PSOE.** Revirtió la exclusión de 2012; no reformó los tramos de activos hasta 2026; no aprobó las leyes de equidad, medicamento y tabaco.

### 11. Qué cambiaría la conclusión
- SISLE por CCAA cruzado con el partido de gobierno; evaluación causal de las exenciones de 2021 y 2026; confirmar o descartar la rotura de la EU-SILC en 2021.

### 12. Limitaciones
- Cobertura parcial de normas estatales [es-cov-measures-health-central]; sin planes estratégicos (salvo hepatitis C), ejecución presupuestaria ni esperas de atención primaria.
- EU-SILC es autodeclarada y con valores muy bajos: mucho peso del ruido.
- Faltan en la KB los gobiernos de Andalucía y Murcia en 2013.

### 13. Fuentes
Ids de la KB citados en el texto. Fuentes externas, consultadas el 26/11/2026:
- BOE: BOE-A-2012-5403, BOE-A-2018-10752, BOE-A-2020-17339, BOE-A-2021-4628, BOE-A-2024-12290, BOE-A-2025-15652, BOE-A-2026-10324.
- Eurostat: hlth_silc_08, hlth_silc_09, hlth_sha11_hf, hlth_rs_prs2.
- Ministerio de Sanidad, SISLE: https://www.sanidad.gob.es/estadEstudios/estadisticas/inforRecopilaciones/listaEspera.htm
- Ministerio de Sanidad, notas de prensa sobre la hepatitis C: https://www.sanidad.gob.es/gabinete/notasPrensa.do?id=3616 y https://www.sanidad.gob.es/gabinete/notasPrensa.do?id=4025
- Diario de Sesiones del Congreso, DSCD-12-PL-144.

## Historial de revisiones

- v1 · 2026-11-26 · Respuesta inicial · Nueva evidencia: 16 normas y eventos, 12 fichas de estudios y datos, 15 series de Eurostat, nota de conocimiento kn-health-coverage-copayments-access.
- v2 · 2026-11-26 · revisión independiente de sesgos · Se corrige que el PP recurriera la LO 1/2023 (solo Vox, STC 92/2024). Se rebaja de "casi seguro" a "probable" el empeoramiento de las esperas con el PSOE y se añade una comparación de SISLE dentro de ventanas sin rotura (con el PP también empeoran los días). Se corrige el salto de médicos en 2019 (+9,5%, no +13,6%). Se retira el dato no trazable de 58 días de consulta en 2011. Se añaden las enfermeras (bajan un 9% desde 2021), la necesidad no cubierta del quintil más pobre y la tendencia de la UE en esperas. Se precisa qué partido gobernaba las CCAA en cada fase (antes: "muchas del PP en 2018-2026"). Se añade el Plan de Hepatitis C de 2015 (omitido) y un steelman de cada parte (progresividad del copago de 2012, contexto de rescate; universalidad, COVID-19). Se deja de atribuir la necesidad dental a normas estatales. Se señala que las barreras por coste ya bajaron en 2015-2018 y una posible rotura de la EU-SILC en 2021.

# ¿Han aumentado o reducido la criminalidad callejera las políticas de izquierdas de la última década en España?

> **Pregunta (literal):** Hay evidencia de que las politicas de izquierdas de los partidos de izquierdas de los ultimos 10 años hayan aumentado o disminuido la criminalidad en las calles de españa?

Respuesta generada por un agente de IA con esta base de conocimiento y revisada por un segundo agente independiente en busca de sesgos y errores (versión 2, datos a 2026-11-26). Los ids entre corchetes enlazan a las entidades de la base (leyes, estudios, eventos); las cifras se calcularon con SQL sobre los datos.

**Aviso:** es un informe automatizado y auditable, no una verdad oficial. Si ves un error o un sesgo, abre un issue.

### Respuesta corta
No hay evidencia causal suficiente para afirmar que las políticas de los gobiernos PSOE (2018-20), PSOE-UP (2020-23) y PSOE-Sumar (2023-) hayan aumentado ni reducido la delincuencia en la calle. Ninguna de esas políticas tiene un estudio con diseño causal en España sobre delincuencia callejera. Los datos descriptivos muestran tendencias mixtas:
- robos y hurtos por habitante en niveles parecidos a 2016-2019;
- suben el homicidio registrado (cifras pequeñas), los delitos sexuales registrados y la cibercriminalidad.

Confianza: es **improbable** (20-40%) que estas políticas, en conjunto, hayan movido la delincuencia callejera más de un 10% en alguna dirección. Es un juicio, no una estimación: con datos agregados no se puede separar su efecto del de otros factores (COVID, crecimiento de la población, turismo, actuación policial), que podrían compensarse. La evidencia es **débil** en general y **disputada** en política por política.

### Hechos clave
- **Balance de Criminalidad 2025** (Interior) [es-event-2026-01-01-balance-criminalidad-2025]:
  - total: 2.474.156 infracciones (+0,8%);
  - convencional: 1.984.908 (−0,2%), 40,4 por 1.000 hab. ("la franja más baja de la serie" según Interior);
  - cibercriminalidad: 489.248 (+5,3%); las estafas informáticas pasaron de 70.178 (2016) a 430.493 (2025);
  - robo con violencia −1,5%, robo en domicilio −8,3%, hurtos −2,3%;
  - homicidios consumados: 376 (+7,7%).
- **Eurostat, delitos registrados por 100.000 hab.** El signo depende del año de inicio; todos los cambios se calcularon en SQL:

| Delito | 2016 | 2019 | 2021 | 2024 | 2016→24 | 2019→24 | 2021→24 |
|---|---|---|---|---|---|---|---|
| Robo con violencia | 135,6 | 140,4 | 112,0 | 129,5 | −4% | −8% | +16% |
| Robo con fuerza | 336,8 | 280,4 | 269,2 | 293,3 | −13% | +5% | +9% |
| Hurto | 435,4 | 436,4 | 305,1 | 450,9 | +4% | +3% | +48% |
| Homicidio | 0,63 | 0,71 | 0,61 | 0,72 | +14% | +1% | +18% |
| Violencia sexual | 18,8 | 27,8 | 30,4 | 40,4 | +115% | +46% | +33% |
| Violación | 2,69 | 3,99 | 4,52 | 10,74 | ×4 | ×2,7 | ×2,4 |
| Drogas | 26,8 | 35,4 | 38,6 | 44,3 | +65% | +25% | +15% |

  - 2020-2021 son años de COVID. Por eso las subidas medidas desde 2021 son sobre todo recuperación; frente a 2019, robos y hurtos están planos.
  - Homicidio: entre 300 y 376 casos al año, con mucha oscilación. Aun así, 2024 tiene la tasa más alta desde 2012.
  - Violación y violencia sexual: la LO 10/2022 rompe la serie, porque lo que antes era "abuso" con penetración pasa a registrarse como agresión [[es-measure-lo-10-2022-libertad-sexual](../../entries/es/measures/es-measure-lo-10-2022-libertad-sexual.md)]. Pero la violencia sexual ya había subido un 62% entre 2016 y 2021, antes de la ley. No se sabe si es por más delitos o por más denuncias.
  - Drogas: la serie refleja sobre todo la actividad policial, no cuánto tráfico o consumo hay.
- **Población**: +2,9 millones de habitantes entre 2016 y 2025. La población nacida en el extranjero creció en 3,8 millones y la nacida en España bajó en 0,9 millones (es-population, es-population-foreign-born). Las tasas por habitante corrigen el tamaño de la población, pero no su composición.
- **Condenas por nacionalidad** (INE, Estadística de Condenados 2025, en [[es-dossier-inmigracion](../../entries/es/dossiers/es-dossier-inmigracion.md)]): 15,3 condenados por 1.000 adultos extranjeros frente a 6,1 por 1.000 españoles. Son tasas brutas, sin ajustar por edad, sexo, renta ni situación administrativa.
- **Barcelona**, única encuesta periódica de victimización de gran muestra [[study-ajuntament-bcn-2024-enquesta-victimitzacio](../../library/study-ajuntament-bcn-2024-enquesta-victimitzacio.md)]: el porcentaje de residentes víctimas de algún delito fue 30,9% en 2019, 23,5% en 2020, 26,7% en 2022 y 29,8% en 2023. Los hechos por 100 residentes pasaron de 65,5 a 68,4 entre 2019 y 2023. Allí la seguridad depende de Mossos d'Esquadra y Guàrdia Urbana, no del Gobierno central.
- **Percepción**: en el CIS de noviembre de 2025, el 6,3% cita la inseguridad ciudadana entre los tres principales problemas de España (1,1% como el primero) [es-event-2025-11-01-cis-3530-inseguridad-ciudadana]. La serie histórica no está en la KB.
- **Medidas penales de los gobiernos de izquierda**:
  - LO 10/2022 ("solo sí es sí"): no tenía disposición transitoria. El CGPJ contó 1.205 rebajas de condena y 121 excarcelaciones hasta septiembre de 2023, en un recuento incompleto [[es-measure-lo-10-2022-libertad-sexual](../../entries/es/measures/es-measure-lo-10-2022-libertad-sexual.md); es-event-2022-11-01-rebajas-ley-solo-si-es-si]. La LO 4/2023 la corrigió con votos de PSOE y PP [[es-measure-lo-4-2023-reforma-libertad-sexual](../../entries/es/measures/es-measure-lo-4-2023-reforma-libertad-sexual.md)].
  - Endurecimientos aprobados con la izquierda en el Gobierno:
    - hurto leve multirreincidente convertido en delito (LO 14/2022, la misma ley que derogó la sedición) [[es-measure-lo-14-2022-sedicion-malversacion](../../entries/es/measures/es-measure-lo-14-2022-sedicion-malversacion.md)];
    - juicio rápido para allanamiento y usurpación (LO 1/2025) [[es-measure-lo-1-2025-eficiencia-justicia](../../entries/es/measures/es-measure-lo-1-2025-eficiencia-justicia.md)];
    - LO 1/2026 de multirreincidencia: proposición de Junts, aprobada en el Congreso con PSOE y PP según la prensa; el voto no está verificado en datos abiertos [[es-measure-lo-1-2026-multirreincidencia](../../entries/es/measures/es-measure-lo-1-2026-multirreincidencia.md)].
  - Reforma de la LO 4/2015 de seguridad ciudadana: tomada en consideración en octubre de 2024 por 176 votos frente a 170 [es-vote-xv-2024-10-29-s071-v001]. La KB no registra que se aprobara.
  - Moción de Vox sobre delincuencia (8-5-2025, no vinculante): rechazada con 32 votos a favor, 179 en contra (PSOE, Sumar, socios) y 138 abstenciones (PP) [es-vote-xv-2025-05-08-s109-v009].
- **Población reclusa** por 100.000 hab.: 164,5 (2009), 146,5 (2012), 116,2 (2021) y 121,8 (2024), unos 59.400 presos. Baja desde 2009, con gobiernos de los dos signos. La KB no tiene ningún estudio sobre las causas de esa bajada.
- **SMI** (prorrateado a 12 pagas, nominal): 859 € (2018) → 1.381 € (2025), +61% [es-minimum-wage-monthly].

### Mecanismos y evidencia, política por política

| Política | Mecanismo | Evidencia causal (otros países salvo que se indique) | Efecto esperado en España |
|---|---|---|---|
| Subida del SMI | Más renta legal (↓ delito) frente a menos empleo juvenil (↑ delito contra la propiedad) | En sentidos opuestos. Fone 2023 (EE. UU., B): un 1% más de salario mínimo eleva un 0,2-0,3% las detenciones de jóvenes de 16-24 años por delitos contra la propiedad [study-fone-2023-minimum-wage-crime]. Agan 2023 (EE. UU., B): menos reincidencia [[study-agan-2023-minimum-wage-eitc-recidivism](../../library/study-agan-2023-minimum-wage-eitc-recidivism.md)]. España, Rebollo-Sanz 2025 (sin revisión por pares): +42% de violencia psicológica en la pareja; no mide delincuencia callejera [study-rebollo-sanz-2025-minimum-wage-psychological-violence-spain] | Incierto en el signo; probablemente pequeño |
| Ingreso Mínimo Vital (2020) | Más renta, menos delito contra la propiedad | Brasil, Bolsa Família (transferencia condicionada): reduce el delito [[study-chioda-2016-bolsa-familia-crime](../../library/study-chioda-2016-bolsa-familia-crime.md)]. Alaska, dividendo universal: efecto neto pequeño [study-watson-2020-universal-cash-crime] | Ligera reducción o ninguna; sin estudio en España |
| Rebajas de la LO 10/2022 | Excarcelación anticipada → riesgo de reincidencia | Italia: cada año de prisión evita 14-18 delitos, sobre todo hurtos y robos, con otro perfil de recluso [[study-buonanno-2013-italian-pardon-incapacitation](../../library/study-buonanno-2013-italian-pardon-incapacitation.md); study-drago-2009-deterrent-effects-prison] | Indetectable en los agregados (121 excarcelados frente a unos 59.000 presos), pero cada reincidencia tiene víctimas concretas. No hay datos de reincidencia |
| Inmigración y regularización (RD 316/2026) | Composición de la población (más jóvenes, varones y personas de renta baja) → ↑ delitos registrados. Estatus legal → ↓ delito de los regularizados | España 1999-2009: asociación provincial positiva, explicada por el capital humano de los inmigrantes (C) [[study-alonso-borrego-2012-immigration-crime-spain](../../library/study-alonso-borrego-2012-immigration-crime-spain.md)]. Italia: la regularización reduce el delito de los regularizados de 1,1% a 0,5% [study-pinotti-2017-clicking-heavens-door]; efecto pequeño y temporal [study-fasani-2018-amnesties-immigrant-crime]. Síntesis en [kn-immigration-crime-legal-status-enforcement] | Efecto composición: posible y pequeño, sin estimar para 2016-2026. Regularización: probable reducción ligera entre los regularizados, sin datos todavía. La mayoría de la inmigración entra por vías regulares y responde al mercado de trabajo; no es solo una decisión del Gobierno |
| Plantilla y despliegue policial | Disuasión e incapacitación | Fuerte: elasticidad de entre −0,1 y −0,7 según el delito [study-draca-2011-police-crime-london-terror; [study-chalfin-2018-us-cities-underpoliced](../../library/study-chalfin-2018-us-cities-underpoliced.md)] | Sin serie de efectivos en la KB: no evaluable |
| Penas más duras (LO 14/2022, LO 1/2026) | Disuasión e incapacitación de multirreincidentes | Disuasión por severidad más débil que por certeza [[study-chalfin-2017-criminal-deterrence-review](../../library/study-chalfin-2017-criminal-deterrence-review.md)]; incapacitación relevante en delitos contra la propiedad (Buonanno) | LO 1/2026: demasiado reciente |

Efectos futuros, solo de las medidas recientes:
- LO 1/2026: posible reducción local del hurto multirreincidente en 1-3 años, si los juzgados la aplican con rapidez (incierto; evidencia moderada sobre incapacitación).
- Regularización de 2026: reducción ligera del delito de los regularizados en 1-5 años (probable; evidencia moderada y de Italia).

### Dónde discrepa la evidencia
- **Año de inicio**: comparado con 2021, el hurto sube un 48% y el robo con violencia un 16%; comparado con 2019, +3% y −8%. Quien dice que "la delincuencia se dispara" suele partir de los años COVID. Quien dice que "está en mínimos" usa el agregado convencional, en el que pesan mucho los delitos más leves.
- **Delitos sexuales**: ¿hay más delitos, más denuncias o solo un cambio de definición? Sin una encuesta nacional de victimización no se puede separar.
- **Inmigración**: hay sobrerrepresentación bruta en las condenas, pero la literatura atribuye gran parte de ella a la composición por edad y sexo y a la situación legal. No hay estimación causal para España después de 2009.
- **SMI**: ¿pesa más el efecto empleo o el efecto renta? No se ha medido en España para la delincuencia.
- **Percepción frente a registros**: la percepción puede reflejar delitos que no se denuncian, la cobertura mediática o puntos concretos (Barcelona, algunas zonas turísticas). Los registros no captan bien ninguno de los tres.

### Qué depende de valores
- Garantías frente a castigo: la reforma de la "ley mordaza", la multirreincidencia, la prisión.
- Cuánto pesan los costes concentrados y visibles (rebajas de condena, multirreincidentes) frente a los efectos medios.
- Si el objetivo es reducir la delincuencia callejera, la evidencia favorece la certeza de la detección (policía) y la incapacitación de multirreincidentes frente a alargar las penas en general, con coste presupuestario y penitenciario. Si el objetivo incluye la integración, la regularización tiene evidencia favorable sobre el delito de los regularizados.

### Partidos: acciones y palabras
- Con la izquierda en el Gobierno se han aprobado endurecimientos (multirreincidencia en 2022 y 2026, juicio rápido por ocupación) y una medida que produjo excarcelaciones (LO 10/2022), corregida en 2023 con votos de PSOE y PP. Las dos cosas son acciones con el mismo rango (ley orgánica).
- El PP se abstuvo en la moción de Vox de 2025 y votó en contra de tramitar la reforma de la ley de seguridad ciudadana.
- Prueba de simetría, con ventanas de igual longitud: durante el periodo del PP (2011→2017) el robo con violencia bajó un 29%, el robo con fuerza un 11%, el hurto un 1% y el homicidio un 20%. Entre 2017 y 2024 las cifras fueron −2%, −4%, +5% y +9%. Tampoco hay estudio que atribuya la bajada a las políticas del PP: coincidió con la salida de la crisis y con una tendencia de descenso en Europa. El mismo criterio que impide atribuir a la izquierda la subida del homicidio o de los delitos sexuales impide atribuir al PP la bajada de los robos.

### Qué cambiaría la conclusión
- Una encuesta nacional de victimización con serie.
- Estudios con variación regional o por cohortes del SMI, el IMV o la regularización sobre delitos contra la propiedad.
- Datos de reincidencia de los excarcelados por la LO 10/2022.
- Una serie de efectivos policiales por provincia.
- Tasas de delito ajustadas por edad, sexo y situación legal según el origen.
- Datos municipales de Interior (Barcelona, Madrid, zonas turísticas) desde 2016.

### Limitaciones
- Son delitos conocidos por la policía y dependen de la propensión a denunciar. Eurostat solo llega hasta 2024.
- 2020-2021 están distorsionados por la COVID.
- No hay comparación con la UE (crim_off_cat no tiene agregado UE-27).
- Muchas palancas (policía autonómica y local, prisiones en Cataluña y País Vasco) no dependen del Gobierno central.
- "Políticas de izquierdas" agrupa medidas heterogéneas, algunas apoyadas también por el PP.

### Fuentes
- Ministerio del Interior, Balance de Criminalidad, cuarto trimestre de 2025: https://estadisticasdecriminalidad.ses.mir.es/publico/portalestadistico/dam/jcr:7d3776cd-9ca4-4c02-8ca4-96b2571dbee4/Balance%20de%20Criminalidad%20Cuarto%20Trimestre%202025.pdf (consultado el 26-11-2026).
- Eurostat crim_off_cat y crim_pris_cap (consultado el 26-11-2026).
- Ajuntament de Barcelona, EVB 2024: https://ajuntament.barcelona.cat/seguretatiprevencio/sites/default/files/2024-07/24_660_Victimitzacio_inf_BCN.PDF (consultado el 26-11-2026).
- CIS, estudio 3530: https://www.cis.es/documents/d/guest/es3530mar_a (consultado el 26-11-2026).
- BOE: BOE-A-2022-14630, BOE-A-2023-10213, BOE-A-2022-21800, BOE-A-2025-76, BOE-A-2026-7966.

## Historial de revisiones

- v1 · 2026-11-26 · respuesta inicial · añadidas 8 series Eurostat de delincuencia/prisión, 5 medidas penales, balance Interior 2025 y 13 estudios causales.
- v2 · 2026-11-26 · revisión independiente de sesgos · Corrección: SMI 2018-2025 +61%, no +54%; población +2,9 millones, no +2,5. Se eliminaron las cifras sin traza en la KB (efectivos policiales, primer trimestre de 2026, serie del CIS 2012-2026, cobertura municipal). La tabla compara años de inicio (2016/2019/2021) para mostrar el rebote post-COVID. Se añadieron la serie de drogas, la composición demográfica y las tasas de condena por nacionalidad (argumento inmigración-delito, steelman), la subida de delitos sexuales anterior a la LO 10/2022 y que el homicidio de 2024 es el más alto desde 2012. Barcelona (EVB) y CIS se verificaron en la fuente primaria y se guardaron en la KB. Prueba de simetría con ventanas iguales (2011-17 frente a 2017-24) en lugar de 2012, pico de la serie. Se quitaron un juicio sin fuente ("su discurso no lo destaca") y la atribución causal de la bajada de presos a la reforma de 2010. La confianza baja de "muy improbable" a "improbable". Se añadieron efectos futuros.

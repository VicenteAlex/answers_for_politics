# ¿Han mejorado o empeorado las regulaciones de vivienda actuales el acceso de los trabajadores al alquiler y a la compra?

> **Pregunta (literal):** Las regulaciones de vivienda actuales han mejorado o empeorado la capacidad de los trabajadores para acceder a alquileres y compra?

Respuesta generada por un agente de IA con esta base de conocimiento y revisada por un segundo agente independiente en busca de sesgos y errores (versión 2, datos a 2026-11-26). Los ids entre corchetes enlazan a las entidades de la base (leyes, estudios, eventos); las cifras se calcularon con SQL sobre los datos.

**Aviso:** es un informe automatizado y auditable, no una verdad oficial. Si ves un error o un sesgo, abre un issue.

### Respuesta corta
El acceso a la vivienda de los trabajadores ha empeorado en la última década. La causa principal es una oferta que no sigue a la demanda (hogares nuevos, población, crédito), y no es atribuible a una regulación concreta. El efecto de las regulaciones depende del grupo:
- **Inquilinos con contrato**: mejoran (**muy probable**, evidencia **fuerte** sobre el precio). Los topes a la actualización y los contratos de 5/7 años abaratan y estabilizan su alquiler; el coste es menos movilidad.
- **Quien busca alquiler en zonas con topes**: efecto neto **incierto** (evidencia **disputada**). Quien firma paga algo menos. Es **probable** que haya menos contratos nuevos y más alquiler de temporada, pero los estudios no coinciden en cuánto. Que los topes a la actualización encarezcan las rentas de entrada es una hipótesis del Banco de España (evidencia **débil**).
- **Quien quiere comprar**: la regulación del alquiler pesa poco. Influyen más la oferta, el crédito (entrada del 20%) y la demanda. Es **probable** que las ayudas a la compra se trasladen en parte al precio donde la oferta es rígida (evidencia **moderada**, de fuera de España).

### Hechos clave
Fuentes: Eurostat EU-SILC y earn_nt_net, INE IPV e IPVA; cálculos en SQL.

| Indicador | 2015-2016 | Último dato | UE-27 (2025) |
|---|---|---|---|
| Jóvenes de 18-34 años que viven con sus padres | 58,9% (2016; 53,0% en 2008) | 68,7% (2025) | 49,8% |
| Edad media de emancipación | 29,4 (2016) | 30,2 (2025) | 26,3 |
| Inquilinos a precio de mercado con gasto en vivienda > 40% de la renta | 43,0% (2016) | 26,8% (2025) | 18,5% (27,0% en 2016) |
| Propietarios con hipoteca con gasto > 40% | 6,7% (2016) | 3,4% (2025) | 4,6% |
| Población en alquiler a precio de mercado | 12,7% (2015) | 17,4% (2025) | 20,8% |
| Precio de compra / salario neto medio (2015 = 100) | 100 | 130 (2023) | — |
| Alquiler de contratos en vigor / salario neto (2015 = 100) | 100 | 105 (2023) | — |

- **Ruptura de serie salarial.** Eurostat marca con "b" el salario de 2024 en earn_nt_net: el neto sube un 11,7% en un año. Por eso las ratios con salario se cortan en 2023. De 2015 a 2023 el precio de compra subió un 47% y el salario neto medio un 13% (nominales). La v1 decía +80% frente a +30% (2015-2025), una ratio de 139 y un alquiler/salario de 97 en 2024; estas cifras mezclaban la ruptura.
- **El año de inicio importa.** 2015 está cerca del mínimo de precios. Con la misma serie, la ratio precio/salario era 179 en 2007 frente a 130 en 2023. El Banco de España sitúa los precios reales de 2026T1 un 12,2% por debajo del máximo de 2007 [[study-bde-2026-informe-anual-2025-vivienda](../../library/study-bde-2026-informe-anual-2025-vivienda.md)]. La compra está hoy más cara respecto al salario que en 2015, pero menos que en 2007. La barrera actual es sobre todo la entrada: los bancos financian en torno al 80% del precio, frente a más del 100% en 2004-2007 [study-khametshin-2024-bde-mercado-alquiler].
- **Alquiler, entrada frente a contratos vigentes.** En 2024 las viviendas que entraban al mercado se alquilaban un 16,5% por encima de la media de los contratos vigentes (6,2% en 2020). Las actualizaciones de contratos vigentes bajaron un 1,7% real anual de media en 2020-2024 [[study-bde-2026-informe-anual-2025-vivienda](../../library/study-bde-2026-informe-anual-2025-vivienda.md)].
- **Oferta y demanda.** En 2021-2025 se terminaron unas 750.000 viviendas menos que hogares se crearon; en 2025 fueron 240.000 hogares y 92.000 viviendas terminadas. En 2014-2022 la población nacida en el extranjero sumó un 4,5% a la población residente y la nacida en España restó un 1,4% [[study-bde-2026-informe-anual-2025-vivienda](../../library/study-bde-2026-informe-anual-2025-vivienda.md); study-khametshin-2024-bde-mercado-alquiler].
- **Caída de la sobrecarga de los inquilinos (43% → 27%).** Hay dos lecturas posibles y estos datos no permiten separarlas:
  - **Mejora real**: en 2022 el IPC subió un 8,4%, las rentas nominales crecieron y las actualizaciones de los contratos vigentes estaban topadas al 2%. El SMI pasó de 859 € en 2018 a 1.260 € en 2023.
  - **Composición**: quien no puede pagar no aparece como inquilino. Los jóvenes que viven con sus padres subieron 10 puntos, y hogares de más renta que antes compraban ahora alquilan.
  - **Matices**: el gran salto (39,4% → 30,6% entre 2022 y 2023) coincide con una proporción de jóvenes en casa casi plana (65,9% → 65,6%), así que la emancipación no lo explica. En la UE la sobrecarga también bajó (27,0% → 18,5%), aunque menos. Eurostat no marca ruptura en esa serie (comprobado el 26-11-2026).
  - **Dato del Banco de España**: su "cerca del 40%" es la media de 2015-2023 (media de la serie en la KB: 39%), no el dato de 2025 [study-khametshin-2024-bde-mercado-alquiler].

### Regulaciones y mecanismos

| Medida | Mecanismo | Evidencia |
|---|---|---|
| Contratos de 5/7 años (RDL 7/2019) [[es-measure-rdl-7-2019-alquiler](../../entries/es/measures/es-measure-rdl-7-2019-alquiler.md)]; topes a la actualización: 2% en 2022-23, 3% en 2024, IRAV desde 2025 [[es-measure-rdl-6-2022-tope-actualizacion-alquiler](../../entries/es/measures/es-measure-rdl-6-2022-tope-actualizacion-alquiler.md)] | Más estabilidad y menos subidas para quien ya alquila, y más poder negociador frente al propietario. Posible respuesta del propietario: subir la renta al firmar | Bajada real de las actualizaciones: dato directo. La brecha entre rentas de entrada y de contratos vigentes se amplió. El Banco de España lo atribuye a la capitalización, pero la brecha también crece cuando suben los precios de mercado con rentas vigentes rígidas. Descriptivo, grado D |
| Topes a nuevos contratos en zonas tensionadas: Ley 12/2023; Cataluña desde el 16-03-2024; 301 municipios en julio de 2025 [[es-measure-ley-12-2023-vivienda](../../entries/es/measures/es-measure-ley-12-2023-vivienda.md); [es-ct-measure-zonas-tensionadas-2024](../../entries/es/measures/es-ct-measure-zonas-tensionadas-2024.md)] | Rentas más bajas para quien firma. Posible menor oferta: venta, temporada o retirada | Ley catalana de 2020: rentas −4% a −6% y **ninguna caída** de contratos ni del parque (registro de fianzas, revisado por pares, grado B) [study-jofre-monseny-2023-catalonia-rent-control]. Con la misma ley, otro estudio ve −10% de contratos nuevos y rentas más altas en el segmento barato (documento de trabajo, B) [study-monras-2023-catalonia-second-generation-rent-control]. Ley 12/2023: −13% de contratos por habitante, con efecto en renta no robusto y tendencias previas no paralelas (preprint, C) [study-perez-garcia-2026-catalonia-2024-rent-control]. Datos de parte interesada, ambos descriptivos (D): Gobierno con datos del Incasòl, rentas −8,9% en Barcelona y sin caída de contratos vigentes, sin metodología publicada; Fedea con anuncios de una fundación ligada a un seguro de impago, precio ofertado +5,7% en Barcelona frente a +10,8% en España, anuncios −22% y ~47% de temporada en Barcelona a comienzos de 2025 [study-pinto-2026-fedea-ley-vivienda-balance]. Menos anuncios o contratos puede ser retirada de oferta o menos rotación |
| Temporada y habitaciones (Llei catalana 11/2025) [[es-ct-measure-ley-11-2025-lloguer-temporada](../../entries/es/measures/es-ct-measure-ley-11-2025-lloguer-temporada.md)] | Cierra la vía de escape de los topes | Sin evaluación (2026) |
| Reserva de suelo para vivienda protegida (del 30% al 40% en nueva urbanización), recargo del IBI de hasta el 150% a viviendas vacías, incentivos en el IRPF (Ley 12/2023) [[es-measure-ley-12-2023-vivienda](../../entries/es/measures/es-measure-ley-12-2023-vivienda.md)] | Más vivienda asequible a largo plazo; puede encarecer o retrasar la promoción libre | Sin evaluación en la KB |
| Suspensión de desahucios de hogares vulnerables (2020-2025) [[es-measure-rdl-11-2020-suspension-desahucios](../../entries/es/measures/es-measure-rdl-11-2020-suspension-desahucios.md)] | Protege al vulnerable que ya alquila; puede elevar la prima de riesgo y los requisitos de acceso (avales, nóminas) | Sin evaluación. Con datos de 2012, en provincias con juzgados más lentos hay algo menos de alquiler (C) [study-mora-sanguinetti-2012-judicial-inefficiency-rental-spain] |
| Bono Alquiler Joven: 250 €/mes, 800 M€ en 2022-2025 [[es-measure-rd-42-2022-bono-alquiler-joven](../../entries/es/measures/es-measure-rd-42-2022-bono-alquiler-joven.md)] | Ayuda al joven; parte va al propietario si la oferta no crece | Francia: 0,78 € de cada euro acabó en la renta [study-fack-2006-french-housing-benefits-rents]; Reino Unido: 60% a dos tercios de un recorte recayó en el propietario [study-gibbons-2006-uk-housing-benefit-incidence]. Sin estudio en España |
| Avales ICO hasta el 100% del precio para la primera vivienda [[es-measure-rdl-5-2023-avales-ico-primera-vivienda](../../entries/es/measures/es-measure-rdl-5-2023-avales-ico-primera-vivienda.md)] | Elimina la barrera de la entrada; empuja la demanda | 8.549 operaciones a 31-10-2025 (BOE), escala pequeña. Help to Buy (Inglaterra): en Londres subieron los precios sin más construcción; con suelo disponible, más construcción [[study-carozzi-2024-help-to-buy](../../library/study-carozzi-2024-help-to-buy.md)] |
| Límites a pisos turísticos (CCAA y ayuntamientos) | Devuelven viviendas al alquiler residencial | Barcelona: Airbnb elevó las rentas un 1,9% y los precios un 4,6% en el barrio medio [study-garcia-lopez-2020-airbnb-barcelona] |
| Planeamiento y suelo; políticas autonómicas de oferta y avales (incluidas las de CCAA del PP) | Determinan la elasticidad de la oferta, factor principal según el Banco de España | **No recogidas ni evaluadas en la KB**: hueco importante |

### Efectos por grupo

| Grupo | Corto plazo (< 1 año) | Medio plazo (1-5 años) | Largo plazo (> 5 años) | Probabilidad / evidencia |
|---|---|---|---|---|
| Inquilinos con contrato | Mejor: subidas por debajo del IPC, estabilidad | Mejor, con menos movilidad laboral | Depende de que el parque en alquiler se mantenga | Muy probable / fuerte (precio), moderada (movilidad) |
| Quien busca alquiler en zonas tensionadas | Renta firmada menor; más competencia por anuncio | Peor si la oferta pasa a venta o temporada; mejor si no se retira | Peor si frena la inversión en alquiler | Incierto / disputada |
| Quien busca alquiler fuera de zonas tensionadas | Rentas de entrada altas (escasez) | Ídem | Ídem | Probable / moderada (oferta), débil (papel de los topes) |
| Hogares de renta baja | Mejor si ya alquilan; peor ante filtros más duros | Peor si no crece el parque social | — | Incierto / débil |
| Compradores primerizos | Los avales ICO y autonómicos facilitan la entrada | Parte de la ayuda acaba en el precio si la oferta es rígida | Lo decide la oferta (suelo, licencias) | Probable / moderada (fuera de España) |
| Propietarios arrendadores | Menos renta y control | Venden, pasan a temporada o se quedan | — | Probable / moderada |
| Presupuesto público | Coste del Bono (800 M€) y riesgo de los avales (hasta 2.500 M€) | — | — | Casi seguro |

### Dónde discrepa la evidencia
- **¿Reducen la oferta los topes catalanes?** Con el registro de fianzas, un estudio no ve caída de contratos ni del parque; otros dos estiman −10% y −13% de contratos nuevos. El punto clave es si menos contratos o anuncios significa menos viviendas o menos rotación, porque los inquilinos se quedan más.
- **¿Por qué la entrada es tanto más cara que los contratos vigentes?** Puede ser cobertura ante los topes futuros (lectura del Banco de España) o simple escasez con rentas vigentes rígidas. Con estos datos no se pueden separar.
- **Precio de compra en Cataluña**: no creció más tras los topes (+26% frente a +31% en España entre 2024T1 y 2026T2), pero la comparación no tiene contrafactual.
- **Inseguridad jurídica** (argumento del PP y de los arrendadores) frente a **protección del inquilino vulnerable** (argumento de sindicatos de inquilinos y partidos de izquierda): no hay medición en España del efecto de la suspensión de desahucios sobre la oferta.

### Qué depende de valores
- El conflicto de fondo es la estabilidad de quien ya alquila frente al acceso de quien llega, y la renta del propietario frente a la del inquilino.
- Si el objetivo es el acceso de quien entra, la evidencia favorece ampliar la oferta (suelo, licencias, vivienda social en alquiler), con coste presupuestario y un plazo de 5-10 años.
- Si el objetivo es evitar el desplazamiento de los residentes y reforzar su poder negociador, los topes cumplen a corto plazo. El coste recae en parte de quienes buscan piso y en los propietarios, y su cuantía está en disputa.

### Partidos: acciones y palabras
- La Ley 12/2023 salió adelante con los votos de PSOE, Unidas Podemos, ERC y EH Bildu. Votaron en contra PP, Vox, Cs, PNV y Junts; estos dos últimos alegaron competencias [[es-dossier-vivienda-alquiler](../../entries/es/dossiers/es-dossier-vivienda-alquiler.md)].
- Zonas tensionadas: las declaran gobiernos del PSC/ERC (Cataluña), PNV-PSE (País Vasco), PSN (Navarra) y PSOE-IU (Asturias). Entre las CCAA del PP solo Galicia lo ha hecho, a petición de A Coruña y Santiago. La Junta de Andalucía (PP) obtuvo la anulación parcial de la Ley 12/2023 (STC 79/2024).
- El PP propone suelo, avales hipotecarios y medidas contra la ocupación. Su proposición sobre urbanismo y suelo se tomó en consideración en abril de 2026 y decayó con la disolución.
- Los decretos de vivienda de 2026 del Gobierno PSOE-Sumar fueron rechazados o derogados en el Congreso.
- Ningún gobierno, estatal ni autonómico, ha cerrado el déficit de oferta.

### Qué cambiaría la conclusión
- Contratos nuevos y rentas por municipio de 2024-2026 (fianzas autonómicas, SERPAVI), comparando zonas tensionadas y no tensionadas, y separando la rotación de la retirada de oferta.
- Un estudio que separe la capitalización de la escasez en la brecha entre rentas de entrada y de contratos vigentes.
- Evaluaciones de incidencia del Bono Alquiler Joven, de los avales ICO y autonómicos, y de las políticas autonómicas de suelo.
- La serie salarial empalmada tras la ruptura de 2024.

### Limitaciones
- **Salarios**: el salario de earn_nt_net tiene una ruptura en 2024, por lo que no hay ratio salario-precio comparable para 2024-2025.
- **Alquiler INE**: el índice mide contratos vigentes y llega a 2024.
- **EU-SILC**: usa la renta del año anterior y excluye a quien no se ha emancipado.
- **Falta en la KB**: los tipos hipotecarios, el planeamiento urbanístico y las políticas autonómicas.
- **Fichas comprobadas solo contra resúmenes**: Fack, Gibbons, Carozzi y Mora-Sanguinetti.

### Fuentes
- Eurostat ilc_lvho07c, ilc_lvho02, ilc_lvps08, yth_demo_030, earn_nt_net (marca "b" en 2024 en https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/earn_nt_net?geo=ES&ecase=P1_NCH_AW100&currency=EUR); todas consultadas el 26-11-2026.
- INE IPV e IPVA; BOE.
- Banco de España, Informe Anual 2025 (cap. 2) y Documento Ocasional 2432.

## Historial de revisiones

- v1 · 2026-11-26 · respuesta inicial · añadidas 8 series EU-SILC/Eurostat, 4 medidas y 5 estudios.
- v2 · 2026-11-26 · revisión independiente de sesgos · Corregidas las ratios salario-precio por la ruptura de serie de earn_nt_net en 2024 (marca "b" de Eurostat): 139 → 130 y alquiler/salario 97 → 105 (2023). Añadida la comprobación de ventana 2007/2015 para la compra. Reequilibrada la lectura de la caída de la sobrecarga: mejora real o composición. Aclarado que el "40%" del Banco de España es la media de 2015-2023. Rebajada la confianza para quien busca alquiler de "probable" a "incierto" y la capitalización a evidencia débil. Avisos de parte interesada aplicados por igual a Incasòl/Gobierno y a Fedea, con grado por estudio. Añadidos los argumentos de cada lado (poder negociador y desplazamiento; inseguridad jurídica), la demanda (hogares, inmigración, crédito), la reserva de suelo, el IBI de vacías, la Llei 11/2025 y la columna de largo plazo. Las 8.549 operaciones ICO ya estaban verificadas en el BOE. Retirada la afirmación sin fuente sobre los tipos de interés.

# Episodio 18 · Cuotas obrero patronales: IMSS, retiro e Infonavit, con el artículo en cada cifra

Jueves de ContadorIA · 19 de noviembre de 2026 · Tercer jueves de la serie
**"Cálculos que se fundamentan solos"**.

Clase práctica: el pago de cuotas de un trabajador **como se hace en la vida
real**. Los seguros del IMSS que se pagan por mes (octubre), el retiro, la
cesantía y vejez y el Infonavit que se pagan por bimestre (septiembre y octubre),
con dos faltas y una incapacidad en el periodo. Con la Ley del Seguro Social, la
Ley del Infonavit, la Ley del SAR y sus reglamentos, que **ahora trae leyes-mx**.
La idea de siempre: **al modelo no le pides el número, le pides el programa que
lo calcula**, para que el resultado se pueda repetir y se pueda auditar.

## Qué hay aquí

| Archivo | Qué es |
|---|---|
| [`proyecto-cuotas-imss/`](proyecto-cuotas-imss/) | La carpeta de trabajo. Ábrela en Claude Desktop (modo Code). |
| [`proyecto-cuotas-imss/CLAUDE.md`](proyecto-cuotas-imss/CLAUDE.md) | Lo específico de este proyecto: el SBC, los topes, los periodos, los días y dónde vigilar las tasas. Importa las reglas generales. |
| [`proyecto-cuotas-imss/reglas-de-la-serie.md`](proyecto-cuotas-imss/reglas-de-la-serie.md) | Las reglas de toda la serie: escribir el script, la huella y el candado. |
| [`proyecto-cuotas-imss/datos/`](proyecto-cuotas-imss/datos/) | El trabajador, la empresa, el periodo, las faltas e incapacidades, y la UMA con su fuente. Ficticios. |
| [`calcular_cuotas_imss.py`](calcular_cuotas_imss.py) | Mi script de referencia (Python 3, sin instalar nada más). El de Claude será distinto; sirve para comparar. |
| [`tasas-2026-referencia.csv`](tasas-2026-referencia.csv) | Mi tabla de tasas, cada una con su artículo y su transitorio. |
| [`dias-por-ramo-referencia.csv`](dias-por-ramo-referencia.csv) | Mi tabla de días: qué resta una falta y qué resta una incapacidad, ramo por ramo. |
| [`prompt-cuotas-imss.md`](prompt-cuotas-imss.md) | El prompt (una línea) y las pruebas. |

**Los datos del trabajador y de la empresa son inventados.** Las tasas y las reglas
no: salen de las leyes vigentes 2026 y sus transitorios, leídos en leyes-mx. Antes
de usarlas con un cliente, compáralas contra la fuente oficial.

## Cómo repetir el ejercicio

1. Ten leyes-mx instalada y actualizada (`npx leyes-mx actualizar`) y reinicia
   Claude Desktop.
2. En Claude Desktop, modo Code, abre la carpeta `proyecto-cuotas-imss/`.
3. Escribe el prompt de [`prompt-cuotas-imss.md`](prompt-cuotas-imss.md).
4. Para correr mi script:
   `python3 calcular_cuotas_imss.py proyecto-cuotas-imss/datos tasas-2026-referencia.csv dias-por-ramo-referencia.csv`
   (agrega `--salario 3000` para la prueba del tope).

## El caso

| | |
|---|---|
| Trabajador | $800 diarios, alta el 05-01-2026 (primer año): 15 días de aguinaldo, 12 de vacaciones, prima del 25% |
| Empresa | Despacho contable, clase I, **prima de riesgo 0.62950%** (de su determinación anual, vigente desde marzo) |
| Pago | El de noviembre de 2026: **octubre** (31 días) por mes y el **quinto bimestre** (61 días) por bimestre |
| Incidencias | **Dos faltas** sin goce de sueldo (8 y 23 de octubre) y **una incapacidad** por enfermedad general de 3 días (13 al 15 de octubre) |

## Qué tiene que salir

| | |
|---|---|
| Factor de integración | 1.0493 = 1 + (15 + 12 × 25%) ÷ 365, a 4 decimales |
| SBC | $839.44 diarios (7.16 UMA) |
| Tope de 25 UMA / 3 UMA | $2,932.75 / $351.93 (UMA 2026: $117.31) |
| Excedente de 3 UMA | $487.51 diarios |
| Días, enfermedades y maternidad | 28 = 31 − 3 de incapacidad (las faltas sí cotizan aquí: LSS art. 31 fr. I) |
| Días, riesgos, invalidez y vida, guarderías | 26 = 31 − 2 faltas − 3 de incapacidad |
| Días, retiro | 59 = 61 − 2 faltas (en la incapacidad sí se paga retiro: LSS art. 31 fr. IV) |
| Días, cesantía y vejez | 56 = 61 − 2 faltas − 3 de incapacidad |
| Días, Infonavit | 59 = 61 − 2 faltas (en la incapacidad del IMSS **sí** se paga: LINFONAVIT art. 29 y RIPAED art. 35 fr. III) |
| Cesantía y vejez, patrón | **7.513%** (transitorio Segundo, DOF 16-12-2020, columna 2026) |
| Pago mensual (octubre) | Patrón $1,969.14 · trabajador $337.91 |
| Pago bimestral (sep-oct) | Patrón $6,998.65 (Infonavit $2,476.35) · trabajador $528.85 |
| **Total patrón** | **$8,967.79** |
| **Total trabajador** | **$866.76** (se le retiene) |
| **Total a enterar** | **$9,834.55** |
| Huella de mi script | `f5a3376aa703` (y `c484840631d2` con $3,000 diarios, topado en 25 UMA) |

La huella del script que escriba Claude va a ser otra. Lo que importa es que **no
cambie entre una corrida y la siguiente**, y que **cambie cuando cambias un dato**.

## Las trampas de la ley

1. **Cesantía y vejez (art. 168).** La tabla del artículo es la de **2030** (11.875%
   desde 4.01 UMA). La de 2026 está en el transitorio Segundo del decreto del
   16-12-2020: 7.513%. Si solo lees el artículo, en este bimestre pagas
   **$2,050.52 de más** por un solo trabajador.
2. **Enfermedades y maternidad (art. 106).** El artículo trae las tasas de 1997
   (13.9% de cuota fija, 6% y 2% sobre el excedente). El transitorio Décimo Noveno
   las movió cada año hasta 2007: 20.40%, 1.10% y 0.40%.
3. **Una falta no resta lo mismo que una incapacidad, ni en la misma ley.** En el
   IMSS (LSS art. 31), la falta menor de 8 días sigue cotizando en enfermedades y
   maternidad, y la incapacidad no paga cuotas, salvo el ramo de retiro. En el
   Infonavit es al revés: la falta se descuenta y en la incapacidad **sí** se paga
   la aportación (LINFONAVIT art. 29; RIPAED art. 35).
4. **El bimestre no está en el artículo.** La LINFONAVIT art. 35 dice que las
   aportaciones se pagan "por mensualidades vencidas". Lo que las mantiene
   bimestrales es el transitorio Sexto del decreto del 06-01-1997 (hasta que la
   Ley del ISSSTE pague por mes), y para el retiro, la cesantía y vejez, el
   transitorio Vigésimo Séptimo de la LSS. La Ley del ISSSTE no está en
   leyes-mx: que la periodicidad siga siendo bimestral se toma de la práctica
   (el SUA), no verificado en la base.

Por eso el `CLAUDE.md` le pide revisar los transitorios antes de usar una tasa, y
citar el artículo de cada día que resta.

## Lo que sigue siendo tuyo

La prima de riesgo sale de la determinación anual de la empresa, y es dato tuyo.
Si una falta fue con o sin goce de sueldo lo dice tu nómina, no la ley. Si tu
cifra no coincide con la del SUA o con la emisión del IMSS, se averigua por qué.
Y la firma. Los textos son informativos y la fuente oficial prevalece.

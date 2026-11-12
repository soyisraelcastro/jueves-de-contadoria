# Episodio 17 · Ajuste anual de ISR de sueldos: de la constancia al cálculo, fundamentado

Jueves de ContadorIA · 12 de noviembre de 2026 · Segundo jueves de la serie
**"Cálculos que se fundamentan solos"**.

Clase práctica: el impuesto anual de un trabajador a partir de su constancia
(LISR art. 97), con la tarifa anual del Anexo 8 de la RMF. La idea de siempre:
**al modelo no le pides el número, le pides el programa que lo calcula**, para que
el resultado se pueda repetir y se pueda auditar. Y la de esta serie: **entre
mejor configurado está tu espacio de trabajo, más corto es el prompt.**

## Qué hay aquí

| Archivo | Qué es |
|---|---|
| [`proyecto-ajuste-anual/`](proyecto-ajuste-anual/) | La carpeta de trabajo. Ábrela en Claude Desktop (modo Code). |
| [`proyecto-ajuste-anual/CLAUDE.md`](proyecto-ajuste-anual/CLAUDE.md) | Lo específico de este proyecto: el art. 97, los tres casos en que no se calcula y cómo entregar. Importa las reglas generales. |
| [`proyecto-ajuste-anual/reglas-de-la-serie.md`](proyecto-ajuste-anual/reglas-de-la-serie.md) | Las reglas que se repiten en todos los proyectos: escribir el script, la huella y el candado. |
| [`proyecto-ajuste-anual/datos/`](proyecto-ajuste-anual/datos/) | La constancia ficticia y la tarifa anual 2026 (Anexo 8, apartado C.II, DOF 2025-12-28). |
| [`calcular_ajuste_anual.py`](calcular_ajuste_anual.py) | Mi script de referencia (Python 3, sin instalar nada más). El de Claude será distinto; sirve para comparar. |
| [`prompt-ajuste-anual.md`](prompt-ajuste-anual.md) | El prompt (una línea) y tres pruebas. |

**Los datos son inventados.** **La tarifa no**: es la del Anexo 8 de la RMF 2026,
apartado C.II, copiada de leyes-mx. Antes de usarla con un cliente, compárala
contra la fuente oficial.

## Cómo repetir el ejercicio

1. Ten leyes-mx instalada (`npx leyes-mx instalar`) y reinicia Claude Desktop.
2. En Claude Desktop, modo Code, abre la carpeta `proyecto-ajuste-anual/`.
3. Escribe el prompt de [`prompt-ajuste-anual.md`](prompt-ajuste-anual.md).
4. Para correr mi script en tu computadora:
   `python3 calcular_ajuste_anual.py proyecto-ajuste-anual/datos/constancia-trabajador-2026-ficticio.csv proyecto-ajuste-anual/datos/tarifa-anual-2026.csv`

El `CLAUDE.md` usa `@reglas-de-la-serie.md` para importar las reglas generales.
Si en tu instalación no se cargan, pega el contenido de ese archivo dentro del
`CLAUDE.md`.

## Qué tiene que salir

| | |
|---|---|
| Ingresos gravados del año | $312,000.00 |
| Renglón de la tarifa | desde $210,403.70, cuota fija $22,282.14 y 21.36% del excedente |
| **Impuesto anual** | **$43,983.11** |
| Retenciones del año | $47,556.23 (11 × $2,383.65 y $21,336.08 de diciembre) |
| **Diferencia** | **$3,573.12 a favor del trabajador** |
| Huella de mi script | `fb2646d4d4f4` (y `2df488448220` con $450,000 de ingresos, donde el trabajador sale del cálculo) |

La huella del script que escriba Claude va a ser otra. Lo que importa es que **no
cambie entre una corrida y la siguiente**, y que **cambie cuando cambias un dato**.

## Lo que esto sí hace y lo que no

**Calcula con los datos que le das, con la tarifa de un archivo, y cita el
artículo de cada cifra.** Está simplificado a propósito: sin subsidio para el
empleo, sin ingresos exentos y sin impuesto local. En un caso real, depurar la
constancia (qué es gravado y qué es exento) es la mitad del trabajo, y es tuyo.
Quién queda fuera del cálculo y la firma también. Los textos son informativos y la
fuente oficial prevalece.

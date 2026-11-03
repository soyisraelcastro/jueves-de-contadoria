# Episodio 15 · Que el cálculo no dependa de la suerte

Clase práctica del 29 de octubre de 2026, preámbulo de la serie de noviembre
**"Cálculos que se fundamentan solos"**.

Le pides a la IA el ISR de tu nómina y te da un número. Hoy, que busca en
internet, lo más probable es que esté bien. ¿Pero cómo lo compruebas sin
rehacerlo? ¿Y el mes que entra, otra vez? La idea del episodio en una línea:
**al modelo no le pides el número, le pides el programa que lo calcula.**

## Qué hay aquí

| Archivo | Qué es |
|---|---|
| [`prompt-calculo-repetible.md`](prompt-calculo-repetible.md) | El prompt de la clase, las tres pruebas que tiene que pasar el script y lo que tiene que salir. |
| [`calcular_isr_sueldos.py`](calcular_isr_sueldos.py) | Mi script de referencia: ISR mensual del art. 96 con la tarifa leída de un archivo, un renglón con fundamento por empleado y la huella del resultado. |
| [`isr-sueldos/`](isr-sueldos/) y [`isr-sueldos.zip`](isr-sueldos.zip) | El mismo cálculo como **skill** de Claude: el script, la tarifa y las instrucciones en un paquete. El .zip es el que se sube a Claude. |
| [`datos/nomina-octubre-2026-ficticio.csv`](datos/nomina-octubre-2026-ficticio.csv) | La nómina de la clase: 13 empleados, octubre de 2026. |
| [`datos/tarifa-art96-2026.csv`](datos/tarifa-art96-2026.csv) | La tarifa mensual del art. 96 para 2026, del Anexo 8 de la RMF. |

**La nómina es inventada.** La comercializadora no existe y los empleados se
llaman Empleado 01 a 13 a propósito. **La tarifa no es inventada**: es la del
Anexo 8 de la RMF 2026, apartado B, fracción V (DOF 28-12-2025), copiada del
PDF del SAT. Antes de usarla con un cliente, compárala tú contra la fuente.

## Cómo repetir el ejercicio

1. En Claude, revisa que esté encendida **"Ejecución de código y creación de
   archivos"** (Configuración, Capacidades).
2. Abre un chat nuevo y sube los dos archivos de `datos/`.
3. Pega el prompt de `prompt-calculo-repetible.md` y corre las tres pruebas.

Para correr mi script en tu computadora (Python 3, sin instalar nada más):

```
python3 calcular_isr_sueldos.py datos/nomina-octubre-2026-ficticio.csv datos/tarifa-art96-2026.csv
```

Para usarlo como skill:

1. Descarga [`isr-sueldos.zip`](isr-sueldos.zip). No lo descomprimas.
2. En Claude: **Configuración → Capacidades → Skills → Subir skill** (en
   español puede decir "Habilidades"), y elige el .zip. Actívala.
3. En un chat nuevo, sube una nómina mensual y pide el ISR del mes.

## Qué tiene que salir

| | |
|---|---|
| Calculados | 12 |
| A revisar (puede aplicar subsidio) | 1, el Empleado 13 |
| **ISR a retener** | **$60,449.61** |
| Con el Empleado 12 sin otras percepciones | **$60,372.71** |
| Huella de mi script | `65720c45d45b` (y `32061291c32c` con el cambio) |

La huella del script que escriba Claude va a ser otra, porque cada script
escribe su CSV a su manera. Lo que importa es que **no cambie entre una
corrida y la siguiente**.

Dos detalles que están ahí a propósito:

- Los **Empleados 02 y 03** ganan con un centavo de diferencia y caen en
  renglones distintos de la tarifa, pero pagan el mismo ISR: 1,011.68. La
  tarifa es continua, y el script lo valida antes de calcular.
- El **Empleado 05** está en el tope del renglón 5 y paga 1,856.85, un
  centavo más que la cuota fija del renglón 6. Ese centavo viene del redondeo
  de la tarifa publicada, no del script.

## Lo que este script sí hace y lo que no

**Aplica la tarifa, igual cada vez, y deja un renglón auditable por
empleado.** No decide qué es gravado y qué es exento, no calcula el subsidio
para el empleo (lo señala) y no sirve para quincenas sin ajustar la tarifa.
La base y la firma siguen siendo tuyas.

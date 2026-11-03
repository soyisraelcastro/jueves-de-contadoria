---
name: isr-sueldos
description: Calcula el ISR mensual a retener por sueldos y salarios en México (art. 96 LISR) con la tarifa 2026 del Anexo 8 de la RMF, corriendo un script que da el mismo resultado cada vez. Úsala cuando el usuario suba una nómina o prenómina mensual (empleado, sueldo y otras percepciones gravadas) y pida el ISR a retener, revisar las retenciones de un mes o comparar contra lo que calculó su sistema de nómina.
---

# ISR de sueldos, con un script

Jueves de ContadorIA, 29 de octubre de 2026. Clase práctica.

Trabajas para un contador público en México. Preparas el cálculo; la base,
la decisión y la firma son del contador.

## La regla de esta skill

**No calculas tú el ISR.** Lo calcula `scripts/calcular_isr_sueldos.py` con la
tarifa de `references/tarifa-art96-2026.csv`. Nunca escribas una tarifa de
memoria ni hagas la aritmética en el texto de tu respuesta.

## Qué necesitas

Un CSV de la nómina mensual con estas columnas:

- `empleado`
- `sueldo_mensual`
- `otras_percepciones_gravadas` (solo la parte gravada; la exenta ya se restó)

Si el archivo trae otros nombres de columna, propón el mapeo y pide
confirmación antes de correr. Si la nómina no es mensual, detente: la tarifa
de esta skill es la mensual (para otros periodos, regla 3.12.2 de la RMF).

## Cómo se corre

```
python3 scripts/calcular_isr_sueldos.py <nomina.csv> references/tarifa-art96-2026.csv resultado-isr.csv
```

Después:

1. Enseña la tabla: empleado, base, renglón de la tarifa, ISR y estatus.
2. Da el total, cuántos se calcularon, cuántos quedan a revisar y la huella.
3. Entrega `resultado-isr.csv` para descargar.
4. Si el usuario pide verificar un renglón, explícalo a mano con los datos de
   la tarifa: base menos límite inferior, por el porcentaje, más la cuota fija.

## Lo que no hace

- No decide qué percepciones son gravadas o exentas. Toma la base que le dan.
- No calcula el subsidio para el empleo: si la base no pasa de $11,492.66, el
  renglón sale como REVISAR y queda fuera del total. Díselo al usuario.
- No sirve para quincenas, semanas o el cálculo anual sin otra tarifa.

## Si la tarifa cambia

Se reemplaza `references/tarifa-art96-2026.csv` con la del Anexo 8 del año
nuevo, con las mismas columnas. El script no se toca. El script valida que la
tarifa no tenga huecos entre renglones y se detiene si los tiene.

Fuente de la tarifa: Anexo 8 de la RMF 2026, apartado B, fracción V, DOF
28-12-2025.

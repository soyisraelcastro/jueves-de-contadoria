# Ajuste anual de ISR de sueldos de un trabajador

@reglas-de-la-serie.md

Las reglas generales están en `reglas-de-la-serie.md`. Aquí solo va lo específico
de este proyecto.

## Qué es

Calcular el impuesto anual de 2026 de un trabajador a partir de su constancia
(LISR art. 97), con la tarifa anual del Anexo 8 de la RMF.

## Antes de calcular

Primero dime si el trabajador entra al cálculo según el artículo 97, y cuál
inciso lo decide. No se hace el cálculo cuando el trabajador:

- empezó a prestar servicios después del 1 de enero, o los dejó antes del 1 de
  diciembre;
- ganó más de $400,000 en el año por estos conceptos;
- avisó por escrito al retenedor que presentará su declaración anual.

Si no entra, dilo y no calcules nada más.

## Datos

- `datos/constancia-trabajador-2026-ficticio.csv`: la constancia.
- `datos/tarifa-anual-2026.csv`: la tarifa anual 2026 (Anexo 8, apartado C.II).
  Verifica que coincida con la que devuelve leyes-mx y usa SIEMPRE este archivo.

## Cómo entregas

Tabla con: ingresos del año, renglón de la tarifa (límite inferior, cuota fija y
porcentaje), impuesto anual, retenciones del año, diferencia, y qué se hace con
ella (a favor: compensación; a cargo: febrero). Más la huella.

# Que el cálculo no dependa de la suerte: el ISR de sueldos con un script

Jueves de ContadorIA · 29 de octubre de 2026 · Clase práctica, preámbulo de
la serie de noviembre "Cálculos que se fundamentan solos".

La idea en una línea: **al modelo no le pides el número, le pides el programa
que lo calcula.** El programa lee la tarifa de un archivo oficial, da el mismo
resultado cada vez que lo corres y dice en cada renglón de dónde salió.
Y como el cálculo se piensa una vez y después solo se ejecuta, gasta una
fracción de los tokens que gastaría pidiéndoselo de cero cada mes.

Necesitas Claude con **"Ejecución de código y creación de archivos"**
encendido (Configuración, Capacidades).

---

## 1. El prompt

Sube al chat los dos archivos, `nomina-octubre-2026-ficticio.csv` y
`tarifa-art96-2026.csv`, y pega esto:

```
No calcules tú el ISR. Escribe un script de Python que lo calcule, córrelo y
enséñame el resultado.

Reglas del script:
1. La tarifa se lee del archivo tarifa-art96-2026.csv (Anexo 8 de la RMF 2026,
   apartado B, fracción V). No escribas ninguna tarifa de memoria.
2. Base gravable = sueldo_mensual + otras_percepciones_gravadas.
3. Por empleado: base, renglón de la tarifa, límite inferior, excedente,
   porcentaje, impuesto marginal, cuota fija, ISR a retener y una columna de
   fundamento con el artículo y el renglón de la tarifa.
4. Montos con Decimal. El impuesto marginal se redondea a centavos, mitad
   hacia arriba.
5. Si la base no pasa de 11,492.66, no calcules el ISR: márcalo REVISAR
   (puede aplicar el subsidio para el empleo) y déjalo fuera del total.
6. Antes de calcular, valida que la tarifa no tenga huecos entre renglones.
   Si los tiene, detente y dime dónde.
7. Al final: cuántos se calcularon, cuántos quedan por revisar, el total y
   una huella SHA-256 (los primeros 12 caracteres) del CSV de resultado.

Entrégame el script para descargar y el CSV de resultado.
```

## 2. Las tres pruebas

Un script no se aprueba porque corrió. Se aprueba porque pasa estas tres:

```
Córrelo otra vez, sin cambiar nada, y compara la huella con la anterior.
```

```
Explícame el renglón del Empleado 04 como si lo calculara a mano, con la
tarifa enfrente.
```

```
Este mes el Empleado 12 no tuvo otras percepciones. Cambia solo ese dato y
vuelve a correr. Dime qué renglones cambiaron.
```

## 3. Qué tiene que salir

| | |
|---|---|
| Empleados | 13 |
| Calculados | 12 |
| A revisar (subsidio) | 1, el Empleado 13 |
| **ISR a retener** | **$60,449.61** |
| Con el Empleado 12 sin otras percepciones | **$60,372.71** |

La prueba a mano del Empleado 04: base 13,950.00, renglón 4.
13,950.00 − 12,598.03 = 1,351.97 × 16% = 216.32 + 1,011.68 = **1,228.00**.

La huella de tu script no va a ser igual a la mía (cada script escribe su CSV
a su manera). Lo que importa es que **tu huella no cambie entre la corrida uno
y la dos**, y que el total sea el de arriba.

Si el total no sale, el problema está en el script, no en los datos: pídele
que te muestre el renglón donde difiere.

## 4. Lo que este script sí hace y lo que no

- **Sí:** aplica la tarifa mensual del art. 96 sobre la base que tú le das,
  igual cada vez, y te deja un renglón auditable por empleado.
- **No:** decide qué es gravado y qué es exento (horas extra, previsión
  social, aguinaldo). Esa base la determinas tú, antes.
- **No:** calcula el subsidio para el empleo. Lo señala.
- **No:** sirve para quincenas o semanas sin ajustar la tarifa (regla 3.12.2
  de la RMF).

Claude escribe y corre el programa. **Tú decides la base y firmas.**

## Fuentes

- Tarifa: Anexo 8 de la RMF 2026, apartado B, fracción V, publicado en el
  DOF el 28 de diciembre de 2025 (sat.gob.mx). Verificada contra el PDF del
  SAT el 29 de octubre de 2026.
- Límite del subsidio para el empleo, $11,492.66 mensuales: decreto firmado el
  30 de diciembre de 2025, en vigor desde el 1 de enero de 2026.

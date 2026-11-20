# El prompt de la clase

**Entre mejor configurado está tu espacio de trabajo, más corto es el prompt.**
Las reglas generales (escribir el script, la huella y el candado) siguen en
`reglas-de-la-serie.md`, igual que la semana pasada. El `CLAUDE.md` de este
proyecto solo dice lo específico: el SBC, los topes, los periodos, los días y
dónde vigilar las tasas.

Con la carpeta `proyecto-cuotas-imss/` abierta en Claude Desktop (modo Code) y
leyes-mx actualizada (`npx leyes-mx actualizar`, para que traiga la LSS, la Ley
del Infonavit, la Ley del SAR y sus reglamentos):

## El prompt

```
Calcula el pago de cuotas de este trabajador.
```

Por las reglas, Claude consulta las leyes en leyes-mx, integra el SBC, separa lo
mensual de lo bimestral, resta las faltas y la incapacidad donde la ley dice, arma
las tablas de días y de tasas con el artículo de cada renglón, escribe un script,
lo corre y te entrega el pago del patrón y del trabajador con su fundamento y una
huella.

## Las pruebas, una por una

```
Córrelo otra vez, sin cambiar nada, y compara la huella con la anterior.
```

```
Cambia el salario diario a $3,000 y vuelve a correrlo.
```

```
¿Por qué la incapacidad sí cuenta para el retiro y para el Infonavit, y las faltas sí cuentan para enfermedades y maternidad? Muéstrame el texto.
```

```
El artículo 35 de la Ley del Infonavit dice que se paga por mes. ¿Por qué lo calculaste por bimestre?
```

```
¿En qué artículo y con qué frase aparece la tasa de cesantía y vejez? Muéstrame el texto.
```

## Cómo comprobar que quedó bien

- Corrido dos veces con los mismos datos, la huella es **la misma**.
- Con $3,000 diarios, el SBC integrado ($3,147.90) rebasa 25 UMA y se **topa en
  $2,932.75** (LSS art. 28).
- Los días: enfermedades y maternidad **28**; riesgos, invalidez y vida y
  guarderías **26**; retiro **59**; cesantía y vejez **56**; Infonavit **59**.
  Cada resta con su artículo (LSS art. 31 fr. I y IV; LINFONAVIT art. 29 y
  RIPAED art. 35).
- La tasa patronal de cesantía y vejez de 2026 es **7.513%**, no 11.875%: la tabla
  del art. 168 es la de 2030, y la de 2026 está en el transitorio Segundo del
  decreto publicado en el DOF el 16-12-2020.
- La cuota fija de enfermedades y maternidad es **20.40% de la UMA**, no 13.9%: el
  art. 106 trae la tasa de 1997, y el transitorio Décimo Noveno de la ley la subió
  hasta 2007. Lo mismo con el excedente: 1.10% patrón y 0.40% trabajador.
- Total patrón **$8,967.79**, trabajador **$866.76**.
- El bimestre sale de dos transitorios (LSS Vigésimo Séptimo y el Sexto del
  decreto de 1997 de la LINFONAVIT), no del art. 35, que dice mensual.

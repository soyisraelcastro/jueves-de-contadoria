# Cuotas obrero patronales de un trabajador (IMSS, retiro e Infonavit)

@reglas-de-la-serie.md

Las reglas generales están en `reglas-de-la-serie.md`. Aquí solo va lo específico
de este proyecto.

## Qué es

Lo que el patrón entera en el pago del periodo de `datos/periodo-de-pago.csv`,
como se paga en la vida real: los seguros que se pagan **por mes** y los que se
pagan **por bimestre**, con las faltas y las incapacidades del periodo, separando
lo que paga el patrón y lo que se le retiene al trabajador.

## Las leyes

Todas están en leyes-mx (`listar_leyes` para ver las siglas):

- **Ley del Seguro Social** y su **reglamento de afiliación, clasificación de
  empresas, recaudación y fiscalización**.
- **Ley del Infonavit** y su **reglamento de inscripción, pago de aportaciones y
  entero de descuentos**.
- **Ley de los Sistemas de Ahorro para el Retiro** y su reglamento.
- **Ley Federal del Trabajo**, para los días de aguinaldo y de vacaciones.

## Orden

1. **El salario base de cotización (SBC).** Intégralo con el aguinaldo y la prima
   vacacional (LSS art. 27; los días, de la LFT arts. 76, 80 y 87). Factor de
   integración redondeado a 4 decimales; SBC a 2 decimales.
2. **Los topes.** Compara el SBC con el límite superior de 25 UMA (LSS art. 28) y
   separa el excedente de 3 UMA (LSS art. 106, fr. II).
3. **Los periodos.** Qué seguros se pagan por mes y cuáles por bimestre, y en qué
   fecha. Cita de dónde sale cada periodo.
4. **Los días.** Para cada ramo, cuántos días cotiza con las faltas y las
   incapacidades de `datos/incidencias-2026.csv` (LSS art. 31; para el Infonavit,
   su ley y su reglamento). Arma `datos/dias-por-ramo.csv`: ramo, periodo, días,
   qué se restó y el artículo.
5. **Las tasas.** Arma `datos/tasas-2026.csv` con una fila por tasa: ramo, quién
   paga, tasa, base (SBC, UMA o excedente), artículo y la frase de la ley de donde
   sale. **Enséñame las dos tablas antes de seguir.**
6. **Las cuotas**, ramo por ramo, con el script.

## Los ramos

Son todos estos; ninguno se queda fuera:

- **Enfermedades y maternidad**: cuota fija y excedente de 3 UMA (art. 106),
  prestaciones en dinero (art. 107) y gastos médicos de pensionados (art. 25).
- **Riesgos de trabajo**: la prima de la empresa, de `datos/empresa-ficticia.csv`.
- **Invalidez y vida** (art. 147).
- **Guarderías y prestaciones sociales** (art. 211).
- **Retiro, cesantía en edad avanzada y vejez** (art. 168).
- **Infonavit**: la aportación patronal, de su ley.

## Ojo con las tasas

- La LSS dice "salario mínimo" donde hoy se usa la UMA. Usa la UMA de
  `datos/indicadores-2026.csv` y cita su fuente tal como viene ahí.
- **Antes de usar una tasa, revisa los transitorios** (`obtener_transitorios`).
  Hay artículos cuyo texto trae una tasa que no es la de 2026: la del artículo
  puede ser la inicial, que ya cambió, o la final, que todavía no llega. Si un
  transitorio cambia la tasa, cita el artículo **y** el transitorio.
- Lo mismo con los **periodos de pago**: un artículo puede decir una
  periodicidad que un transitorio todavía no deja aplicar. Revisa los
  transitorios de cada ley antes de decidir qué se paga por mes y qué por
  bimestre.
- Una falta y una incapacidad no restan igual, ni en todos los ramos, ni en
  las dos leyes. No supongas: cada resta lleva su artículo.

## Datos

- `datos/trabajador-2026-ficticio.csv`: el trabajador y sus prestaciones.
- `datos/empresa-ficticia.csv`: la clase y la prima de riesgo de la empresa.
- `datos/periodo-de-pago.csv`: el mes y el bimestre que se pagan.
- `datos/incidencias-2026.csv`: faltas e incapacidades del periodo.
- `datos/indicadores-2026.csv`: la UMA, con su fuente.

## Cómo entregas

1. El SBC: factor, SBC, tope de 25 UMA y excedente de 3 UMA.
2. Los días de cada ramo, con lo que se restó y por qué.
3. Una tabla por ramo: tasa, base, días, cuota patronal, cuota obrera y
   fundamento.
4. Dos subtotales, el pago mensual y el bimestral, y los totales: patrón,
   trabajador (lo que se le retiene) y total a enterar.
5. La huella.

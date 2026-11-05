# Episodio 16 · Declaración mensual con Claude: el cálculo y el artículo que lo sustenta

Jueves de ContadorIA · 5 de noviembre de 2026 · Primer jueves de la serie
**"Cálculos que se fundamentan solos"**.

Clase práctica: la declaración de octubre (pago provisional de ISR y pago
mensual de IVA de una persona moral), con el artículo que sustenta cada cifra.
Sin teoría de por medio: el proyecto ya está configurado y el prompt es de una
línea.

La idea en una línea, la misma de la clase anterior: **al modelo no le pides el
número, le pides el programa que lo calcula.** Así el resultado se **puede
repetir** y se **puede auditar**: el script queda guardado, lo revisas una vez,
y mismo archivo de datos da siempre la misma huella.

Antes de empezar se instala **leyes-mx**, la base gratuita y abierta de leyes
fiscales y laborales de México que Claude lee desde tu computadora en lugar de
contestar de memoria: [leyes.todoconta.com](https://leyes.todoconta.com).

## Cómo se trabaja: la carpeta es el proyecto

**Claude Desktop, en modo Code, trabaja con los archivos directamente en tu
computadora**, sin subirlos a un project del chat. Le abres una **carpeta** (o
directorio) y esa carpeta es el proyecto: ahí están tus datos, lo que Claude
genera y sus instrucciones.

**`CLAUDE.md` es el archivo que dice de qué va el proyecto**: el objetivo, las
reglas y los límites. Claude lo lee al empezar cada sesión. Según la
documentación de Claude Code, son archivos de texto con instrucciones
persistentes; como cada sesión arranca desde cero, es lo que le da memoria al
proyecto: lo escribes una vez y se aplica siempre. Ventajas:

- **Se escribe una vez** y no hay que repetir las reglas en cada prompt.
- **Es un archivo de texto**: lo lees, lo corriges y lo compartes con tu
  equipo copiando la carpeta.
- **Los prompts quedan cortos**, porque las reglas ya están puestas.

Para que funcione bien, escríbelo concreto y comprobable ("cita el artículo de
cada cifra", no "sé cuidadoso") y corto: la recomendación es menos de unas 200
líneas. Aviso honesto: la documentación lo trata como contexto, no como
configuración obligatoria. Claude lo sigue muy bien cuando está claro, pero
no es un candado técnico, así que la cita se revisa siempre.

## Qué hay aquí

| Archivo | Qué es |
|---|---|
| [`proyecto-declaracion-mensual/`](proyecto-declaracion-mensual/) | La carpeta de trabajo: las reglas en `CLAUDE.md` y los datos en `datos/`. Ábrela en Claude Desktop (modo Code). |
| [`proyecto-declaracion-mensual/CLAUDE.md`](proyecto-declaracion-mensual/CLAUDE.md) | Las instrucciones del proyecto: escribir el script en lugar de dar el número, consultar leyes-mx, citar cada cifra, decir "no verificado" y no inventar datos. Es el candado. |
| [`calcular_declaracion_mensual.py`](calcular_declaracion_mensual.py) | Mi script de referencia (Python 3, sin instalar nada más): lee el CSV, calcula, deja un renglón por concepto con su fundamento e imprime la huella. El de Claude va a ser distinto; sirve para comparar. |
| [`proyecto-declaracion-mensual/datos/datos-octubre-2026-ficticio.csv`](proyecto-declaracion-mensual/datos/datos-octubre-2026-ficticio.csv) | Los datos de la clase. |
| [`prompt-declaracion-mensual.md`](prompt-declaracion-mensual.md) | El prompt (una línea) y tres pruebas para seguir. |

**Los datos son inventados.** La comercializadora no existe. Lo que sí es real
es la ley: LISR arts. 9 y 14, LIVA arts. 1, 4, 5-D y 6, en su texto vigente de
2026.

## Cómo repetir el ejercicio

1. Instala leyes-mx: `npx leyes-mx instalar`. Reinicia Claude Desktop por
   completo (sal y vuelve a abrir). Necesitas Node 20 o superior.
2. En Claude Desktop, modo Code, abre la carpeta `proyecto-declaracion-mensual/`.
3. Escribe el prompt de [`prompt-declaracion-mensual.md`](prompt-declaracion-mensual.md).
4. Para correr mi script de referencia en tu computadora:
   `python3 calcular_declaracion_mensual.py proyecto-declaracion-mensual/datos/datos-octubre-2026-ficticio.csv`

Lo probado en la clase es **Claude Desktop en modo Code**. leyes-mx no funciona
en claude.ai por el navegador, por ahora.

## Qué tiene que salir

| | |
|---|---|
| Utilidad fiscal para el pago provisional | $1,050,000.00 (0.10 × $10,500,000) |
| Menos pérdida fiscal pendiente | $900,000.00 |
| ISR al 30% | $270,000.00 |
| **Pago provisional de ISR** | **$43,800.00** (menos $225,000 y $1,200) |
| Sin la pérdida fiscal | $88,800.00 |
| Huella de mi script | `3a9360387128` (y `f21276489da0` sin la pérdida fiscal) |
| IVA causado | $160,000.00 |
| **Pago mensual de IVA** | **$60,000.00** (menos $96,000 y $4,000) |

La huella del script que escriba Claude va a ser otra, porque cada script arma
su tabla a su manera. Lo que importa es que **no cambie entre una corrida y la
siguiente**, y que **cambie cuando cambias un dato**.

Las dos declaraciones se presentan a más tardar el **17 de noviembre** (LISR
art. 14 y LIVA art. 5-D).

## Lo que esto sí hace y lo que no

**Calcula con los datos que le das y cita el artículo de cada cifra.** No decide
tu coeficiente de utilidad, qué pérdidas aplican, ni qué IVA es acreditable
(art. 5 LIVA): eso lo decides tú. leyes-mx no trae la Miscelánea fiscal (salvo
el Anexo 8), jurisprudencia ni criterios del SAT; si preguntas por algo de eso,
contesta "no verificado". Los textos son informativos y la fuente oficial (DOF y
Cámara de Diputados) prevalece. La firma sigue siendo tuya.

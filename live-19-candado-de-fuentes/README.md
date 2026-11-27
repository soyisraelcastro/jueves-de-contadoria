# Episodio 19 · Ponle candado a las fuentes: que no invente el criterio fiscal

Jueves de ContadorIA · 26 de noviembre de 2026 · Cierre de la serie **"Cálculos que
se fundamentan solos"**.

El candado es el conjunto de reglas que le pones a Claude para que **cite solo lo
que le diste y diga "no sé" cuando no está**. Aquí está escrito como un archivo:
[`CLAUDE.md`](CLAUDE.md). Lo pegas en la carpeta de cualquier proyecto y las
reglas aplican siempre; no hay que repetirlas en cada prompt.

## Qué hay aquí

| Archivo | Qué es |
|---|---|
| [`CLAUDE.md`](CLAUDE.md) | El candado: las cinco reglas, la segunda vuelta y lo que no resuelve. Cópialo a tu carpeta de trabajo. |
| [`segunda-vuelta-ejemplo.md`](segunda-vuelta-ejemplo.md) | La respuesta con una cita alterada que se audita en la clase, y lo que tiene que salir. |

## Cómo usarlo

1. Crea una carpeta de trabajo y copia ahí [`CLAUDE.md`](CLAUDE.md).
2. Ábrela en Claude Desktop (modo Code), con leyes-mx instalada y actualizada
   (`npx leyes-mx actualizar`).
3. Haz las tres pruebas de la clase, con prompts de una línea.

## Las tres trampas

**Uno: un artículo que no existe.**

```
¿Qué dice el artículo 9999 de la LISR?
```

Lo correcto: **"no verificado"**, sin inventar.

**Dos: algo que no está en la base.**

```
¿Qué dice la jurisprudencia de la Suprema Corte sobre la deducción de pérdidas por créditos incobrables?
```

leyes-mx trae las leyes, sus reglamentos y la Resolución Miscelánea Fiscal 2026,
pero no la jurisprudencia ni los criterios del SAT. Lo correcto: dice que no lo
tiene y **pregunta si quieres que lo busque fuera**; no lo busca por su cuenta.

**Tres: una reforma publicada que todavía no aplica.**

```
Aplica la reforma de la LISR de 2027 al pago provisional de noviembre de 2026.
```

La reforma se publicó en el DOF el 13 de noviembre de 2026, pero **entra en vigor
el 1 de enero de 2027**. Lo correcto: te dice que para noviembre de 2026 sigue la
ley de 2026 y no aplica la reforma. Publicada no es lo mismo que vigente.

El resultado depende del modelo del día. Si alguna prueba no sale como se espera, es
justo el caso para la segunda vuelta.

## La segunda vuelta

Un chat nuevo, sin el contexto del primero, revisa cada cita contra la fuente:

```
Audita estas citas contra las fuentes.
```

y pegas la respuesta del primer chat. Para practicar, usa
[`segunda-vuelta-ejemplo.md`](segunda-vuelta-ejemplo.md): trae una cita alterada
que tiene que salir **NO VERIFICADA**.

## Lo que esto sí hace y lo que no

Reduce lo que tienes que revisar y te dice dónde termina lo comprobable. **No
decide si el artículo aplica a tu caso, no sabe lo que no está en las fuentes y no
sustituye tu firma.** Según la documentación de Claude Code, un `CLAUDE.md` es
contexto y no configuración obligatoria: Claude lo sigue muy bien cuando está
claro, pero no es una garantía técnica, así que la cita se revisa siempre.

# El prompt de la clase

**Entre mejor configurado está tu espacio de trabajo, más corto es el prompt.**
La semana pasada las reglas vivían dentro del `CLAUDE.md`. Hoy las reglas
generales (escribir el script, la huella, el candado) están en su propio archivo,
`reglas-de-la-serie.md`, y el `CLAUDE.md` del proyecto solo dice lo específico de
este cálculo.

Con la carpeta `proyecto-ajuste-anual/` abierta en Claude Desktop (modo Code) y
leyes-mx instalada:

## El prompt

```
Haz el ajuste anual de este trabajador.
```

Por las reglas, Claude consulta leyes-mx, decide primero si el trabajador entra al
cálculo (art. 97), escribe un script, lo corre y te entrega la tabla con el
fundamento de cada cifra y una huella.

## Las pruebas, una por una

```
Córrelo otra vez, sin cambiar nada, y compara la huella con la anterior.
```

```
Cambia los ingresos gravados a $450,000 y vuelve a correrlo.
```

```
Explícame renglón por renglón por qué da diferencia a favor.
```

## Cómo comprobar que quedó bien

- El script queda guardado en `resultados/` y lo puedes abrir y revisar.
- Corrido dos veces con los mismos datos, la huella es **la misma**.
- Con $450,000 de ingresos, el trabajador **sale del cálculo** (art. 97, inciso b)
  y el resultado lo dice en lugar de calcular.
- La tarifa sale del archivo `tarifa-anual-2026.csv`, no de memoria. Compárala
  contra la que devuelve leyes-mx.

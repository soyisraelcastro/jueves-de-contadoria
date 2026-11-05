# Los prompts de la clase

La idea de la serie: **al modelo no le pides el número, le pides el programa que
lo calcula.** Así el resultado se puede repetir y se puede auditar.

**Entre mejor configurado está tu espacio de trabajo, más corto es el prompt.** La clase pasada el prompt traía reglas numeradas; hoy las reglas viven en la carpeta y el prompt es una línea.

Con la carpeta `proyecto-declaracion-mensual/` abierta en Claude Desktop
(modo Code) y leyes-mx instalada, los prompts son cortos: las reglas (incluida
la de escribir el script) ya viven en `CLAUDE.md` y los datos en `datos/`.

## El prompt

```
Calcula la declaración de octubre de 2026.
```

Por las reglas del `CLAUDE.md`, Claude consulta leyes-mx, escribe un script, lo
corre y te entrega la tabla con el fundamento de cada cifra y una huella.

## Para seguir en la clase

Las tres pruebas, una por una:

```
Córrelo otra vez, sin cambiar nada, y compara la huella con la anterior.
```

```
Quita la pérdida fiscal de los datos y vuelve a correrlo.
```

```
¿En qué fracción dice la ley que se resta la pérdida fiscal? Muéstrame el texto.
```

## Cómo comprobar que quedó bien

- El script queda guardado en `resultados/`, y lo puedes abrir y revisar.
- Corrido dos veces con los mismos datos, la huella es **la misma**.
- Cambias un dato y la huella **cambia**.
- Cada renglón trae ley, artículo, vigencia y última reforma.
- Si le pides algo que no está en la base, contesta "no verificado" y te
  pregunta si lo busca fuera. No lo busca solo.

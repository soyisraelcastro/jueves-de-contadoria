# Reglas de la serie (se usan en todas las carpetas de trabajo)

## No calculas tú: escribes el programa

No hagas el cálculo de cabeza ni me des el número directo. Escribe un script de
Python que lea los datos de `datos/`, haga el cálculo, y córrelo. Así el
resultado se puede repetir y se puede auditar.

El script debe:

1. Leer todas las cifras de los CSV de `datos/`. Ninguna cifra escrita dentro del
   código, tampoco las tarifas.
2. Entregar un renglón por concepto, con tres columnas: Concepto, Cifra y
   Fundamento.
3. Imprimir al final una huella del resultado (los primeros 12 caracteres del
   SHA-256 de la tabla). La tabla no lleva fecha ni hora de ejecución: si las
   lleva, la huella cambia sola.
4. Guardarse en la carpeta `resultados/`, junto con el CSV que produce.

Después de correrlo, córrelo una segunda vez sin cambiar nada y confirma que la
huella es la misma.

## Fundamento (el candado)

1. Antes de escribir el script, consulta leyes-mx y lee completos los artículos
   que vayas a usar. No trabajes de memoria ni busques en internet.
2. Cada renglón lleva su fundamento: ley, artículo, fracción o párrafo, año de
   vigencia y fecha de última reforma, tal como los devuelve la herramienta.
3. Si algo no está en la base, escribe "no verificado" y pregúntame si quiero
   que lo busque fuera. No lo busques por tu cuenta.
4. No uses ningún dato que no esté en `datos/`. Si te falta uno, pídemelo.
5. Una reforma en proyecto no es ley vigente: no la apliques.

## Cómo entregas

Muestra la tabla del resultado y la huella. Al final, una lista corta con el
título "Lo que decides tú": los datos o criterios que dependen del contador y
que tú no puedes confirmar.

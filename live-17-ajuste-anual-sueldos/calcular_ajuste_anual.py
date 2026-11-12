#!/usr/bin/env python3
"""
Ajuste anual de ISR de sueldos de un trabajador (LISR art. 97), con la tarifa
anual del Anexo 8 de la RMF 2026 (apartado C.II) leída de un archivo.

Mi script de referencia para la clase del 12 de noviembre de 2026. No lleva
cifras escritas: la constancia y la tarifa salen de los CSV. Cada renglón del
resultado trae su fundamento y al final imprime una huella: mismos datos,
misma huella.

Los artículos y la tarifa se leyeron con leyes-mx (texto vigente 2026, descargado
el 2026-11-02). Antes de usarlo con un cliente, compara contra la fuente oficial.

Uso:
    python3 calcular_ajuste_anual.py proyecto-ajuste-anual/datos/constancia-trabajador-2026-ficticio.csv proyecto-ajuste-anual/datos/tarifa-anual-2026.csv
"""
import csv
import hashlib
import sys
from datetime import date
from decimal import ROUND_HALF_UP, Decimal

LISR97 = "LISR art. 97 (vigencia 2026, última reforma DOF 2024-04-01)"
TARIFA = "Anexo 8 RMF 2026, apartado C.II (DOF 2025-12-28), LISR arts. 97 y 152"
TOPE_INGRESOS = Decimal("400000")  # LISR art. 97, inciso b)


def dinero(x: Decimal) -> Decimal:
    return x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def leer_constancia(ruta: str) -> dict[str, str]:
    with open(ruta, newline="", encoding="utf-8") as f:
        return {r["concepto"]: r["valor"] for r in csv.DictReader(f)}


def leer_tarifa(ruta: str) -> list[tuple[Decimal, Decimal | None, Decimal, Decimal]]:
    with open(ruta, newline="", encoding="utf-8") as f:
        return [
            (Decimal(r["limite_inferior"]), Decimal(r["limite_superior"]) if r["limite_superior"] else None,
             Decimal(r["cuota_fija"]), Decimal(r["porcentaje_excedente"]))
            for r in csv.DictReader(f)
        ]


def fuera_del_calculo(c: dict[str, str]) -> str | None:
    """Devuelve el inciso del art. 97 que deja fuera al trabajador, o None."""
    inicio = date.fromisoformat(c["fecha_inicio_servicios"])
    fin = date.fromisoformat(c["fecha_fin_servicios"]) if c["fecha_fin_servicios"] else None
    if inicio > date(2026, 1, 1) or (fin is not None and fin < date(2026, 12, 1)):
        return "inciso a): inició después del 1 de enero o dejó de prestar servicios antes del 1 de diciembre"
    if Decimal(c["ingresos_gravados_2026"]) > TOPE_INGRESOS:
        return "inciso b): ingresos anuales de más de $400,000"
    if c["aviso_por_escrito_declaracion_anual"].strip().lower() == "si":
        return "inciso c): avisó por escrito que presentará su declaración anual"
    return None


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    c = leer_constancia(sys.argv[1])
    tarifa = leer_tarifa(sys.argv[2])
    filas: list[tuple[str, str, str]] = []

    causa = fuera_del_calculo(c)
    if causa:
        filas.append(("Entra al cálculo", "no", f"{LISR97}, {causa}"))
    else:
        filas.append(("Entra al cálculo", "si", f"{LISR97}, no se actualiza ningún inciso de exclusión"))
        base = Decimal(c["ingresos_gravados_2026"]) - Decimal(c["impuesto_local_retenido"])
        filas.append(("Ingresos gravados del año", str(dinero(base)), f"{LISR97}, párrafo segundo"))
        li, ls, cuota, pct = next(r for r in tarifa if r[0] <= base and (r[1] is None or base <= r[1]))
        excedente = dinero(base - li)
        impuesto = dinero(cuota + excedente * pct / 100)
        filas.append(("Renglón: límite inferior", str(li), TARIFA))
        filas.append(("Renglón: cuota fija", str(cuota), TARIFA))
        filas.append(("Renglón: porcentaje sobre el excedente", str(pct), TARIFA))
        filas.append(("Excedente del límite inferior", str(excedente), TARIFA))
        filas.append(("Impuesto anual", str(impuesto), f"{LISR97}, párrafo segundo y art. 152"))
        retenido = dinero(Decimal(c["retenciones_enero_a_noviembre"]) + Decimal(c["retencion_diciembre"]))
        filas.append(("Retenciones del año", str(retenido), f"{LISR97}, párrafo segundo (pagos provisionales del art. 96)"))
        dif = dinero(impuesto - retenido)
        if dif < 0:
            filas.append(("Diferencia a favor del trabajador", str(-dif),
                          f"{LISR97}, se compensa contra la retención de diciembre y las siguientes, a más tardar dentro del año de calendario posterior"))
        else:
            filas.append(("Diferencia a cargo del trabajador", str(dif), f"{LISR97}, se entera a más tardar en febrero"))

    texto = "concepto,cifra,fundamento\n" + "\n".join(f'"{a}",{b},"{d}"' for a, b, d in filas) + "\n"
    print(texto, end="")
    print(f"huella,{hashlib.sha256(texto.encode('utf-8')).hexdigest()[:12]},mismos datos = misma huella")


if __name__ == "__main__":
    main()

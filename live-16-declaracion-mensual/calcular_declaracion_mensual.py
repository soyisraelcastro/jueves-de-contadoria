#!/usr/bin/env python3
"""
Declaración mensual de una persona moral (régimen general): pago provisional de
ISR (LISR art. 14) y pago mensual de IVA (LIVA art. 5-D).

Mi script de referencia para la clase del 5 de noviembre de 2026. No lleva cifras
escritas: todo sale del CSV de datos. Cada renglón del resultado trae su
fundamento (ley, artículo, fracción), y al final imprime una huella del
resultado: mismo archivo de datos, misma huella.

Los artículos y su vigencia se leyeron con leyes-mx (texto vigente 2026,
descargado el 2026-11-02). Antes de usarlo con un cliente, compara el texto
contra la fuente oficial.

Uso:
    python3 calcular_declaracion_mensual.py proyecto-declaracion-mensual/datos/datos-octubre-2026-ficticio.csv
"""
import csv
import hashlib
import sys
from decimal import ROUND_HALF_UP, Decimal

CENTAVO = Decimal("0.01")
TASA_ISR = Decimal("0.30")  # LISR art. 9
TASA_IVA = Decimal("0.16")  # LIVA art. 1

LISR = "LISR (vigencia 2026, última reforma DOF 2024-04-01)"
LIVA = "LIVA (vigencia 2026, última reforma DOF 2021-11-12)"


def dinero(x: Decimal) -> Decimal:
    return x.quantize(CENTAVO, rounding=ROUND_HALF_UP)


def leer(ruta: str) -> dict[str, Decimal]:
    with open(ruta, newline="", encoding="utf-8") as f:
        datos = {r["concepto"]: Decimal(r["valor"]) for r in csv.DictReader(f)}
    esperados = [
        "ingresos_nominales_enero_octubre_2026", "utilidad_fiscal_2025", "ingresos_nominales_2025",
        "perdidas_fiscales_pendientes", "ptu_pagada_2026", "pagos_provisionales_enero_septiembre_2026",
        "retenciones_art_54_octubre", "valor_actos_octubre_tasa_16", "iva_acreditable_octubre",
        "iva_retenido_octubre", "saldo_a_favor_iva_meses_anteriores",
    ]
    faltan = [k for k in esperados if k not in datos]
    if faltan:
        sys.exit(f"Faltan datos: {', '.join(faltan)}")
    return datos


def calcular(d: dict[str, Decimal]) -> list[tuple[str, Decimal, str]]:
    r: list[tuple[str, Decimal, str]] = []

    # ISR: pago provisional, LISR art. 14
    coef = (d["utilidad_fiscal_2025"] / d["ingresos_nominales_2025"]).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
    r.append(("ISR coeficiente de utilidad", coef, f"{LISR}, art. 14, fr. I"))
    utilidad = dinero(coef * d["ingresos_nominales_enero_octubre_2026"])
    r.append(("ISR utilidad fiscal para el pago provisional", utilidad, f"{LISR}, art. 14, fr. II"))
    base = utilidad - d["ptu_pagada_2026"] - d["perdidas_fiscales_pendientes"]
    r.append(("ISR menos PTU pagada", d["ptu_pagada_2026"], f"{LISR}, art. 14, fr. II, inciso a)"))
    r.append(("ISR menos pérdidas fiscales pendientes", d["perdidas_fiscales_pendientes"], f"{LISR}, art. 14, fr. II, inciso c)"))
    r.append(("ISR base del pago provisional", dinero(base), f"{LISR}, art. 14, fr. II"))
    isr = dinero(base * TASA_ISR)
    r.append(("ISR al 30%", isr, f"{LISR}, art. 14, fr. III y art. 9"))
    r.append(("ISR menos pagos provisionales anteriores", d["pagos_provisionales_enero_septiembre_2026"], f"{LISR}, art. 14, fr. III"))
    r.append(("ISR menos retenciones del periodo", d["retenciones_art_54_octubre"], f"{LISR}, art. 14, fr. III y art. 54"))
    pago_isr = isr - d["pagos_provisionales_enero_septiembre_2026"] - d["retenciones_art_54_octubre"]
    r.append(("ISR pago provisional de octubre", dinero(pago_isr), f"{LISR}, art. 14, fr. III"))

    # IVA: pago mensual, LIVA art. 5-D
    causado = dinero(d["valor_actos_octubre_tasa_16"] * TASA_IVA)
    r.append(("IVA causado al 16%", causado, f"{LIVA}, art. 1"))
    r.append(("IVA menos acreditable del mes", d["iva_acreditable_octubre"], f"{LIVA}, art. 4"))
    r.append(("IVA menos retenido en el mes", d["iva_retenido_octubre"], f"{LIVA}, art. 5-D"))
    r.append(("IVA menos saldo a favor de meses anteriores", d["saldo_a_favor_iva_meses_anteriores"], f"{LIVA}, art. 6"))
    pago_iva = causado - d["iva_acreditable_octubre"] - d["iva_retenido_octubre"] - d["saldo_a_favor_iva_meses_anteriores"]
    r.append(("IVA pago mensual de octubre", dinero(pago_iva), f"{LIVA}, art. 5-D"))
    return r


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    filas = calcular(leer(sys.argv[1]))
    salida = ["concepto,cifra,fundamento"] + [f'"{c}",{v},"{f}"' for c, v, f in filas]
    texto = "\n".join(salida) + "\n"
    print(texto, end="")
    huella = hashlib.sha256(texto.encode("utf-8")).hexdigest()[:12]
    print(f"huella,{huella},mismo archivo de datos = misma huella")


if __name__ == "__main__":
    main()

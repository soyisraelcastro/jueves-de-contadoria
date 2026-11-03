"""ISR mensual de sueldos y salarios (art. 96 LISR), siempre con el mismo resultado.

Jueves de ContadorIA · 29 de octubre de 2026 · Clase práctica.

Uso:
    python3 calcular_isr_sueldos.py nomina.csv tarifa-art96-2026.csv [resultado.csv]

La tarifa NO vive en este archivo: se lee del CSV, copiado del Anexo 8 de la
RMF 2026, apartado B, fracción V (DOF 28-12-2025). Si la tarifa cambia, se
cambia el CSV y el script queda igual.

Lo que NO calcula: el subsidio para el empleo. Si la base no pasa del límite
del decreto (DOF 31-12-2025), el renglón sale como REVISAR y no entra al total.
"""

import csv
import hashlib
import sys
from decimal import ROUND_HALF_UP, Decimal

FUENTE_TARIFA = "Art. 96 LISR; Anexo 8 RMF 2026, ap. B, fr. V"
LIMITE_SUBSIDIO = Decimal("11492.66")  # Decreto del subsidio para el empleo, DOF 31-12-2025
CENTAVO = Decimal("0.01")


def pesos(texto):
    return Decimal(texto.replace(",", "").strip() or "0")


def redondea(monto):
    return monto.quantize(CENTAVO, rounding=ROUND_HALF_UP)


def lee_tarifa(ruta):
    with open(ruta, newline="", encoding="utf-8-sig") as f:
        renglones = [
            {
                "renglon": int(r["renglon"]),
                "li": pesos(r["limite_inferior"]),
                "ls": pesos(r["limite_superior"]) if r["limite_superior"].strip() else None,
                "cuota": pesos(r["cuota_fija"]),
                "tasa": pesos(r["porcentaje_excedente"]) / 100,
            }
            for r in csv.DictReader(f)
        ]
    # La tarifa tiene que ser continua: cada límite inferior es el superior anterior más un centavo.
    for antes, despues in zip(renglones, renglones[1:]):
        if antes["ls"] is None or despues["li"] != antes["ls"] + CENTAVO:
            sys.exit(f"La tarifa tiene un hueco entre los renglones {antes['renglon']} y {despues['renglon']}.")
    return renglones


def renglon_de(base, tarifa):
    for r in tarifa:
        if base >= r["li"] and (r["ls"] is None or base <= r["ls"]):
            return r
    sys.exit(f"Ninguna tarifa cubre la base {base}.")


def calcula(nomina, tarifa):
    filas = []
    for e in nomina:
        base = pesos(e["sueldo_mensual"]) + pesos(e["otras_percepciones_gravadas"])
        r = renglon_de(base, tarifa)
        excedente = base - r["li"]
        marginal = redondea(excedente * r["tasa"])
        isr = r["cuota"] + marginal
        revisar = base <= LIMITE_SUBSIDIO
        filas.append({
            "empleado": e["empleado"],
            "base_gravable": f"{base:.2f}",
            "renglon_tarifa": r["renglon"],
            "limite_inferior": f"{r['li']:.2f}",
            "excedente": f"{excedente:.2f}",
            "porcentaje": f"{r['tasa'] * 100:.2f}",
            "impuesto_marginal": f"{marginal:.2f}",
            "cuota_fija": f"{r['cuota']:.2f}",
            "isr_a_retener": "" if revisar else f"{isr:.2f}",
            "estatus": "REVISAR: puede aplicar subsidio para el empleo" if revisar else "CALCULADO",
            "fundamento": f"{FUENTE_TARIFA}, renglón {r['renglon']}",
        })
    return filas


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    tarifa = lee_tarifa(sys.argv[2])
    with open(sys.argv[1], newline="", encoding="utf-8-sig") as f:
        nomina = list(csv.DictReader(f))
    filas = calcula(nomina, tarifa)

    salida = sys.argv[3] if len(sys.argv) > 3 else "resultado-isr.csv"
    with open(salida, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)

    for x in filas:
        print(f"{x['empleado']:<12} base {Decimal(x['base_gravable']):>12,.2f}  "
              f"renglón {x['renglon_tarifa']:>2}  ISR {x['isr_a_retener'] or '—':>10}  {x['estatus']}")

    calculados = [x for x in filas if x["estatus"] == "CALCULADO"]
    total = sum(Decimal(x["isr_a_retener"]) for x in calculados)
    with open(salida, "rb") as f:
        huella = hashlib.sha256(f.read()).hexdigest()[:12]
    print()
    print(f"Calculados: {len(calculados)} · A revisar: {len(filas) - len(calculados)}")
    print(f"ISR a retener (calculados): {total:,.2f}")
    print(f"Huella del resultado: {huella}  (misma entrada, misma huella)")
    print(f"Resultado en {salida}")


if __name__ == "__main__":
    main()

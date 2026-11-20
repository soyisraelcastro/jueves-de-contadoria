#!/usr/bin/env python3
"""
Cuotas obrero patronales de un trabajador, como se pagan en la vida real: la
cédula de noviembre de 2026, con los seguros mensuales de octubre y los
bimestrales (retiro, cesantía y vejez e Infonavit) del quinto bimestre, con las
faltas y la incapacidad del periodo.

Mi script de referencia para la clase del 19 de noviembre de 2026. No lleva
cifras escritas: el trabajador, la empresa, el periodo, las incidencias y la UMA
salen de los CSV de datos; las tasas y las reglas de días, de los CSV de
referencia, cada renglón con su fundamento. Al final imprime una huella del
resultado: mismos datos, misma huella.

Los artículos y los transitorios se leyeron con leyes-mx (LSS vigente 2026,
última reforma DOF 2026-01-15). Antes de usarlo con un cliente, compara el texto
contra la fuente oficial.

Uso:
    python3 calcular_cuotas_imss.py proyecto-cuotas-imss/datos tasas-2026-referencia.csv dias-por-ramo-referencia.csv
    python3 calcular_cuotas_imss.py ... --salario 3000
"""
import csv
import hashlib
import sys
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

CENT = Decimal("0.01")
DIEZMIL = Decimal("0.0001")


def r(x, q=CENT):
    return x.quantize(q, rounding=ROUND_HALF_UP)


def lee(path, llave="concepto"):
    with open(path, newline="", encoding="utf-8") as f:
        return {row[llave]: row for row in csv.DictReader(f)}


def filas_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    datos, tasas_csv, dias_csv, *resto = sys.argv[1:]
    d = Path(datos)
    t = lee(d / "trabajador-2026-ficticio.csv")
    emp = lee(d / "empresa-ficticia.csv")
    per = lee(d / "periodo-de-pago.csv")
    ind = lee(d / "indicadores-2026.csv")
    incid = filas_csv(d / "incidencias-2026.csv")
    num = lambda tabla, k: Decimal(tabla[k]["valor"])

    salario = Decimal(resto[1]) if resto[:1] == ["--salario"] else num(t, "salario_diario")
    uma = num(ind, "uma_diaria")
    variables = {"prima_riesgo_trabajo": num(emp, "prima_riesgo_trabajo") / 100}

    # 1. SBC (LSS art. 27; LFT arts. 76, 80 y 87) y topes (LSS arts. 28 y 106)
    factor = r(1 + (num(t, "dias_aguinaldo") + num(t, "dias_vacaciones") * num(t, "prima_vacacional")) / 365, DIEZMIL)
    sbc_integrado = r(salario * factor)
    tope = r(uma * 25)
    sbc = min(sbc_integrado, tope)
    tres_uma = r(uma * 3)
    excedente = max(sbc - tres_uma, Decimal(0))
    veces_uma = sbc / uma

    filas = [
        ("Salario diario", salario, "datos/trabajador-2026-ficticio.csv"),
        ("Factor de integración", factor, "LSS art. 27; LFT arts. 76, 80 y 87 (4 decimales)"),
        ("SBC integrado", sbc_integrado, "LSS art. 27"),
        ("Tope de 25 UMA", tope, "LSS art. 28; UMA: " + ind["uma_diaria"]["fuente"]),
        ("SBC (con tope)", sbc, "LSS art. 28"),
        ("3 UMA", tres_uma, "LSS art. 106 fr. II"),
        ("Excedente de 3 UMA", excedente, "LSS art. 106 fr. II"),
    ]

    # 2. Días que cotiza cada grupo de ramos (LSS art. 31)
    meses = {"mes": per["mes"]["valor"], "bimestre": per["bimestre"]["valor"]}
    total_dias = {"mes": num(per, "dias_del_mes"), "bimestre": num(per, "dias_del_bimestre")}

    def suma(tipo, periodo):
        return sum((Decimal(i["dias"]) for i in incid
                    if i["tipo"] == tipo and i["fecha_inicio"][:7] in meses[periodo].split("/")), Decimal(0))

    ausencias = {p: suma("ausencia", p) for p in total_dias}
    incapacidades = {p: suma("incapacidad", p) for p in total_dias}
    if any(v >= 8 for v in ausencias.values()):
        sys.exit("Hay ausencias de 8 días o más: el patrón queda liberado si da la baja (LSS art. 31 fr. I y art. 37). "
                 "Ese caso no se resuelve con esta regla.")

    reglas = filas_csv(dias_csv)
    dias, periodo_de = {}, {}
    for g in reglas:
        p = g["periodo"]
        n = total_dias[p]
        if g["resta_ausencias"] == "si":
            n -= ausencias[p]
        if g["resta_incapacidades"] == "si":
            n -= incapacidades[p]
        dias[g["grupo"]] = n
        periodo_de[g["grupo"]] = p
        filas.append((f"Días que cotiza: {g['grupo']} ({p})", n, g["fundamento"]))

    # 3. Cuotas, ramo por ramo
    bases = {"sbc": sbc, "uma": uma, "excedente": excedente}
    tot = {(c, q): Decimal(0) for c in total_dias for q in ("patron", "trabajador")}
    for row in filas_csv(tasas_csv):
        if row["ramo"].startswith("Cesantía") and row["quien"] == "patron" and veces_uma <= 4:
            sys.exit(f"El SBC es {veces_uma:.2f} UMA: la tasa de cesantía de la tabla de referencia es la de "
                     "4.01 UMA en adelante. Toma el renglón que corresponde del transitorio Segundo (DOF 16-12-2020).")
        tasa = variables.get(row["tasa"]) or Decimal(row["tasa"])
        n = dias[row["dias"]]
        importe = r(bases[row["base"]] * tasa * n)
        tot[(periodo_de[row["dias"]], row["quien"])] += importe
        quien = "patrón" if row["quien"] == "patron" else "trabajador"
        filas.append((f"{row['ramo']} ({quien}, {tasa * 100:.5f}% sobre {row['base']}, {n} días)", importe, row["fundamento"]))

    for p, nombre in (("mes", f"Pago mensual ({meses['mes']})"), ("bimestre", f"Pago bimestral ({meses['bimestre']})")):
        filas += [
            (f"{nombre}: patrón", tot[(p, "patron")], ""),
            (f"{nombre}: trabajador (se retiene)", tot[(p, "trabajador")], ""),
        ]
    patron = tot[("mes", "patron")] + tot[("bimestre", "patron")]
    trabajador = tot[("mes", "trabajador")] + tot[("bimestre", "trabajador")]
    filas += [
        ("Total patrón", patron, per["pago"]["valor"]),
        ("Total trabajador (se retiene)", trabajador, per["pago"]["valor"]),
        ("Total a enterar", patron + trabajador, per["pago"]["valor"]),
    ]

    salida = Path("resultados")
    salida.mkdir(exist_ok=True)
    csv_out = salida / "cuotas.csv"
    with open(csv_out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Concepto", "Cifra", "Fundamento"])
        w.writerows((c, str(v), fu) for c, v, fu in filas)

    ancho = max(len(c) for c, _, _ in filas)
    for c, v, fu in filas:
        print(f"{c:<{ancho}}  {v:>12}  {fu}")
    print(f"\nSBC = {veces_uma:.2f} UMA")
    print("Huella:", hashlib.sha256(csv_out.read_bytes()).hexdigest()[:12])


if __name__ == "__main__":
    main()

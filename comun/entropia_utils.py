import math
from collections import Counter


def frecuencias_bytes(datos: bytes) -> Counter:
    return Counter(datos)


def entropia_shannon(frecuencias: Counter, total: int) -> float:
    if total == 0:
        return 0.0
    entropia = 0.0
    for cantidad in frecuencias.values():
        p_i = cantidad / total
        entropia -= p_i * math.log2(p_i)
    return entropia


def redundancia(entropia: float, base_bits: int = 8) -> float:
    if base_bits == 0:
        return 0.0
    return 1 - (entropia / base_bits)


def resumen_entropia(path: str) -> dict:
    with open(path, "rb") as f:
        datos = f.read()
    total = len(datos)
    frecs = frecuencias_bytes(datos)
    h = entropia_shannon(frecs, total)
    r = redundancia(h)
    return {
        "path": path,
        "tamanio_bytes": total,
        "frecuencias": frecs,
        "entropia_bits_simbolo": h,
        "redundancia": r,
    }


def graficar_histograma_comparativo(res_a: dict, res_b: dict, titulo: str,
                                     salida_png: str, label_a: str = None,
                                     label_b: str = None) -> None:
    import matplotlib
    matplotlib.use("Agg")  # sin entorno gráfico interactivo
    import matplotlib.pyplot as plt

    label_a = label_a or res_a["path"]
    label_b = label_b or res_b["path"]

    ejes_x = list(range(256))
    ya = [res_a["frecuencias"].get(i, 0) for i in ejes_x]
    yb = [res_b["frecuencias"].get(i, 0) for i in ejes_x]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)

    ax1.bar(ejes_x, ya, width=1.0, color="#1F4E79")
    ax1.set_title(f"{label_a}  |  H = {res_a['entropia_bits_simbolo']:.4f} bits/símbolo"
                   f"  |  {res_a['tamanio_bytes']} bytes")
    ax1.set_ylabel("Frecuencia")

    ax2.bar(ejes_x, yb, width=1.0, color="#C00000")
    ax2.set_title(f"{label_b}  |  H = {res_b['entropia_bits_simbolo']:.4f} bits/símbolo"
                   f"  |  {res_b['tamanio_bytes']} bytes")
    ax2.set_xlabel("Valor de byte (0-255)")
    ax2.set_ylabel("Frecuencia")

    fig.suptitle(titulo, fontsize=13, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(salida_png, dpi=120)
    plt.close(fig)
    print(f"[OK] Histograma guardado en: {salida_png}")


def imprimir_resumen(res: dict, nombre_amigable: str = None) -> None:
    nombre = nombre_amigable or res["path"]
    print(f"--- {nombre} ---")
    print(f"  Tamaño          : {res['tamanio_bytes']} bytes")
    print(f"  Entropía H(S)   : {res['entropia_bits_simbolo']:.4f} bits/símbolo")
    print(f"  Redundancia R   : {res['redundancia']*100:.2f} %")
    print(f"  Símbolos únicos : {len(res['frecuencias'])} / 256")

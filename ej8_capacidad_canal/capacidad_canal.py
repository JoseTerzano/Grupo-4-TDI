import math


# =====================================================================
# a) Ingreso y validación de la matriz del canal P(Y|X)  (2x4)
# =====================================================================
def leer_matriz_canal() -> list:
    print("Ingrese la matriz de transición P(Y|X) del canal (2 filas x 4 columnas).")
    print("Cada fila corresponde a un símbolo de entrada (X=0, X=1); cada")
    print("columna a un símbolo de salida (Y=0,1,2,3). Cada fila debe sumar 1.\n")

    matriz = []
    for fila_idx in range(2):
        while True:
            try:
                entrada = input(
                    f"  Fila X={fila_idx} (4 valores separados por espacio o coma): "
                ).strip().replace(",", " ")
                valores = [float(v) for v in entrada.split()]
                if len(valores) != 4:
                    print("    [ERROR] Se requieren exactamente 4 valores. Reintente.")
                    continue
                if any(v < 0 or v > 1 for v in valores):
                    print("    [ERROR] Las probabilidades deben estar entre 0 y 1. Reintente.")
                    continue
                if abs(sum(valores) - 1.0) > 1e-6:
                    print(f"    [ERROR] La fila suma {sum(valores):.4f}, debe sumar "
                          f"exactamente 1. Reintente.")
                    continue
                matriz.append(valores)
                break
            except ValueError:
                print("    [ERROR] Entrada no numérica. Reintente.")
    return matriz


def matriz_de_ejemplo() -> list:
    """Canal de ejemplo válido, usado si el usuario no quiere tipear a mano."""
    return [
        [0.7, 0.2, 0.05, 0.05],   # P(Y|X=0)
        [0.05, 0.05, 0.2, 0.7],   # P(Y|X=1)
    ]


# =====================================================================
# c) Cálculo de Información Mutua para una distribución de entrada dada
# =====================================================================
def log2(x: float) -> float:
    return math.log2(x) if x > 0 else 0.0


def entropia(probs: list) -> float:
    return -sum(p * log2(p) for p in probs if p > 0)


def calcular_informacion_mutua(matriz: list, p_x0: float) -> dict:
    p_x1 = 1 - p_x0
    p_x = [p_x0, p_x1]

    # P(Y) por Teorema de la Probabilidad Total: P(y) = sum_x P(x) P(y|x)
    p_y = [sum(p_x[i] * matriz[i][j] for i in range(2)) for j in range(4)]

    h_y = entropia(p_y)                                    # H(Y)
    h_y_dado_x = sum(p_x[i] * entropia(matriz[i]) for i in range(2))  # H(Y|X)
    i_xy = h_y - h_y_dado_x                                 # I(X;Y) = H(Y) - H(Y|X)

    return {"p_x0": p_x0, "p_x1": p_x1, "p_y": p_y,
            "h_y": h_y, "h_y_dado_x": h_y_dado_x, "i_xy": i_xy}


# =====================================================================
# b), d) y e) Búsqueda exhaustiva y maximización
# =====================================================================
def buscar_capacidad_canal(matriz: list, paso: float = 0.01) -> dict:
    mejor = {"i_xy": -1.0}
    p = 0.0
    n_pasos = round(1.0 / paso)
    for k in range(n_pasos + 1):
        p_x0 = round(k * paso, 10)
        resultado = calcular_informacion_mutua(matriz, p_x0)
        if resultado["i_xy"] > mejor["i_xy"]:
            mejor = resultado
    return mejor


def main():
    print("=== a) Carga de la matriz del canal ===")
    usar_ejemplo = input(
        "¿Desea ingresar la matriz manualmente? (s/n, 'n' usa un ejemplo): "
    ).strip().lower()
    if usar_ejemplo == "s":
        matriz = leer_matriz_canal()
    else:
        matriz = matriz_de_ejemplo()
        print("Usando matriz de ejemplo:")
        for i, fila in enumerate(matriz):
            print(f"  P(Y|X={i}) = {fila}")

    print("\n=== b), c) y d) Búsqueda exhaustiva (paso 0.01) ===")
    mejor = buscar_capacidad_canal(matriz, paso=0.01)

    print("\n=== e) Resultado final ===")
    print(f"  Capacidad del Canal C = {mejor['i_xy']:.6f} bits/símbolo")
    print(f"  Lograda con P(X=0) = {mejor['p_x0']:.2f}  y  P(X=1) = {mejor['p_x1']:.2f}")
    print(f"  P(Y) en ese punto óptimo = "
          f"[{', '.join(f'{v:.4f}' for v in mejor['p_y'])}]")
    print(f"  H(Y) = {mejor['h_y']:.4f} bits ; H(Y|X) = {mejor['h_y_dado_x']:.4f} bits")

    # Referencia analítica opcional: si el canal es binario simétrico "puro"
    # (2 salidas), se podría comparar contra C = 1 - H(p). Para 4 salidas no
    # hay fórmula cerrada general; por eso se resuelve por búsqueda exhaustiva.


if __name__ == "__main__":
    main()

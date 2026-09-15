
# =====================================================================
# a) Distancia de Hamming
# =====================================================================
def distancia_hamming(s1: str, s2: str) -> int:
    if len(s1) != len(s2):
        raise ValueError(
            f"Hamming no aplicable: longitudes distintas ({len(s1)} vs {len(s2)}). "
            "Hamming solo compara símbolo a símbolo en la MISMA posición; "
            "un desfase (inserción/eliminación) desalinea todo lo que sigue."
        )
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))


# =====================================================================
# b) Distancia de Levenshtein (Distancia de Edición) - Programación Dinámica
# =====================================================================
def distancia_levenshtein(s1: str, s2: str) -> int:
    n, m = len(s1), len(s2)
    if n == 0:
        return m
    if m == 0:
        return n

    # dp[i][j] = distancia de edición entre s1[:i] y s2[:j]
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = i           # borrar los i primeros caracteres de s1
    for j in range(m + 1):
        dp[0][j] = j           # insertar los j primeros caracteres de s2

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            costo_sustitucion = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,                    # eliminación
                dp[i][j - 1] + 1,                    # inserción
                dp[i - 1][j - 1] + costo_sustitucion  # sustitución (o coincidencia)
            )
    return dp[n][m]


# =====================================================================
# d) Heurística propuesta para comparación de texto "aproximada"
# =====================================================================
def son_similares(s1: str, s2: str, umbral: float = 0.85) -> tuple:
    """
    Heurística propuesta:
      1. Normalizar ambas cadenas: minúsculas + sin espacios extra.
      2. Calcular la distancia de Levenshtein normalizada:
             similitud = 1 - distancia / max(len(s1), len(s2))
      3. Considerar "mismo dato" (típicamente un error de tipeo) si la
         similitud supera un umbral configurable (ej. 0.85 = 85%).
    Esta normalización evita declarar "distinto" a textos que solo difieren
    en mayúsculas/minúsculas o espacios, y es tolerante a 1-2 errores de
    tipeo en cadenas medianas/largas, sin sobre-exigir una coincidencia
    exacta como lo haría Hamming.
    """
    a = s1.strip().lower()
    b = s2.strip().lower()
    dist = distancia_levenshtein(a, b)
    largo_max = max(len(a), len(b), 1)
    similitud = 1 - dist / largo_max
    return similitud >= umbral, similitud, dist


# =====================================================================
# main / demostración
# =====================================================================
def main():
    print("=== a) Distancia de Hamming ===")
    s1, s2 = "Juan Perez", "Jaun Perez"
    d = distancia_hamming(s1, s2)
    print(f'  "{s1}" vs "{s2}" (misma longitud={len(s1)})  ->  Hamming = {d}')
    print("  (aquí sí es aplicable porque ambas cadenas tienen longitud 10;")
    print("   detecta la transposición 'ua'->'au' como 2 posiciones distintas)")

    print("\n  Ahora un caso con longitudes distintas (inserción/eliminación):")
    s3, s4 = "Horacio López", "Oracio López"
    print(f'  "{s3}" (len={len(s3)}) vs "{s4}" (len={len(s4)})')
    try:
        distancia_hamming(s3, s4)
    except ValueError as e:
        print(f"  [ERROR esperado] {e}")

    print("\n=== b) y c) Distancia de Levenshtein ===")
    dl = distancia_levenshtein(s3, s4)
    print(f'  "{s3}" vs "{s4}"  ->  Levenshtein = {dl} '
          f"(1 eliminación de la 'H' inicial + 1 sustitución 'o'->'O' por may/min)")

    pares_prueba = [
        ("Juan Perez", "Jaun Perez"),
        ("Horacio López", "Oracio López"),
        ("computadora", "computdora"),
        ("teoria de la informacion", "teoría de la información"),
    ]
    print("\n  Más ejemplos:")
    for a, b in pares_prueba:
        print(f'    "{a}" vs "{b}"  ->  Levenshtein = {distancia_levenshtein(a, b)}')

    print("\n=== d) Heurística de comparación aproximada ===")
    for a, b in pares_prueba:
        similar, sim, dist = son_similares(a, b)
        print(f'    "{a}" vs "{b}"  ->  similitud={sim*100:.1f}%  '
              f'({"MISMO DATO (probable error de tipeo)" if similar else "DATOS DISTINTOS"})')


if __name__ == "__main__":
    main()

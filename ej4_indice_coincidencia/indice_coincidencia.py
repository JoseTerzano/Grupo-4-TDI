import sys
import os
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "comun"))
from entropia_utils import resumen_entropia, frecuencias_bytes

ALFABETO_ES = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"  # 27 letras
SIN_TILDE = str.maketrans("ÁÉÍÓÚÜ", "AEIOUU")


def indice_coincidencia(frecuencias, n_total: int) -> float:
    """
    IC = sum( f_i * (f_i - 1) ) / ( N * (N - 1) )
    """
    if n_total < 2:
        return 0.0
    numerador = sum(f * (f - 1) for f in frecuencias.values())
    denominador = n_total * (n_total - 1)
    return numerador / denominador


def frecuencias_letras(datos: bytes) -> Counter:
    """
    Frecuencias sobre el alfabeto español de 27 letras: pasa a mayúsculas,
    quita tildes (conserva la Ñ) y descarta todo lo que no sea letra
    (espacios, puntuación, números, saltos de línea).
    Permite comparar el IC contra la referencia teórica de 0.074.
    """
    texto = datos.decode("utf-8", errors="ignore").upper().translate(SIN_TILDE)
    return Counter(c for c in texto if c in ALFABETO_ES)


def analizar_archivo(path: str) -> dict:
    if not os.path.isfile(path):
        raise FileNotFoundError(f"No se encontró el archivo: {path}")
    with open(path, "rb") as f:
        datos = f.read()
    n = len(datos)
    frecs = frecuencias_bytes(datos)
    ic = indice_coincidencia(frecs, n)
    res = resumen_entropia(path)  # reutiliza el cálculo de entropía del ejercicio 3
    res["ic"] = ic

    letras = frecuencias_letras(datos)
    n_letras = sum(letras.values())
    res["n_letras"] = n_letras
    res["ic_letras"] = indice_coincidencia(letras, n_letras)
    return res


def main():
    if len(sys.argv) >= 2:
        rutas = sys.argv[1:]
    else:
        entrada = input(
            "Ingrese la(s) ruta(s) de archivo separadas por coma "
            "(ej: texto.txt, texto.zip): "
        ).strip()
        rutas = [r.strip() for r in entrada.split(",") if r.strip()]

    resultados = []
    print("=== Índice de Coincidencia (IC) vs Entropía ===\n")
    for ruta in rutas:
        try:
            res = analizar_archivo(ruta)
        except FileNotFoundError as e:
            print(f"[ERROR] {e}")
            continue
        resultados.append(res)
        print(f"--- {ruta} ---")
        print(f"  Tamaño       : {res['tamanio_bytes']} bytes")
        print(f"  Entropía H(S): {res['entropia_bits_simbolo']:.4f} bits/símbolo")
        print(f"  IC (bytes)   : {res['ic']:.5f}   <- 256 símbolos posibles")
        print(f"  IC (letras)  : {res['ic_letras']:.5f}   <- solo A-Z + Ñ "
              f"({res['n_letras']} letras)")
        print()

    if resultados:
        print("Referencia teórica:")
        print("  IC (letras) texto en español   -> ≈ 0.074")
        print("  IC (letras) texto aleatorio    -> ≈ 1/27 = 0.037")
        print("  IC (bytes)  archivo aleatorio  -> ≈ 1/256 = 0.0039")
        print("""
Por qué hay dos IC:
  El IC por bytes cuenta también espacios, puntuación, saltos de línea y
  los bytes de las tildes UTF-8. Eso reparte la probabilidad entre más
  símbolos y baja el IC, por lo que NO es comparable con 0.074. El IC por
  letras usa el mismo alfabeto de 27 letras que la referencia teórica.""")
        print("""
Comparación conceptual entre IC y Entropía:
  Ambos son medidas de qué tan "desigual" es la distribución de símbolos,
  pero mientras la Entropía H(S) = -Σ p_i·log2(p_i) mide la incertidumbre
  promedio (en bits) que aporta cada símbolo nuevo, el Índice de
  Coincidencia mide directamente la probabilidad de choque entre dos
  símbolos tomados al azar del mismo texto.
  Cuanto MÁS desigual es la distribución (más redundante, menos aleatorio
  el texto) -> MENOR es la entropía, pero MAYOR es el IC (hay más
  probabilidad de que dos letras cualquiera coincidan, porque unas pocas
  letras dominan). Un archivo comprimido o cifrado, al ser casi uniforme,
  tiende a un IC bajo (cercano a 1/256 para bytes, o 1/27 para letras) y a
  una entropía cercana a su máximo teórico. Esta relación inversa es
  justamente la base del criptoanálisis clásico: el IC permite detectar la
  longitud de la clave en cifrados polialfabéticos como Vigenère, buscando
  el corrimiento que maximiza el parecido con el IC esperado del idioma.
""")


if __name__ == "__main__":
    main()

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "comun"))
from entropia_utils import resumen_entropia, imprimir_resumen


# =====================================================================
# a) Frecuencia relativa y entropía  (ya implementado en comun/entropia_utils.py,
#    reutilizado aquí: frecuencias_bytes() hace UN solo recorrido -> O(N))
# =====================================================================

def analizar_archivo(path: str) -> dict:
    if not os.path.isfile(path):
        raise FileNotFoundError(f"No se encontró el archivo: {path}")
    res = resumen_entropia(path)
    imprimir_resumen(res, path)
    return res


# =====================================================================
# main
# =====================================================================
def main():
    if len(sys.argv) >= 2:
        rutas = sys.argv[1:]
    else:
        entrada = input(
            "Ingrese la ruta del archivo a analizar (o dos rutas separadas "
            "por coma para comparar, ej: texto.txt, texto.zip): "
        ).strip()
        rutas = [r.strip() for r in entrada.split(",") if r.strip()]

    print("\n=== a) Entropía empírica por archivo ===")
    resultados = []
    for ruta in rutas:
        try:
            resultados.append(analizar_archivo(ruta))
        except FileNotFoundError as e:
            print(f"[ERROR] {e}")

    # b) y c) Comparación .txt vs comprimido, si se dieron 2 o más archivos
    if len(resultados) >= 2:
        print("\n=== b) y c) Comparación y explicación ===")
        for r in resultados:
            print(f"  {r['path']}: H = {r['entropia_bits_simbolo']:.4f} bits/símbolo "
                  f"(redundancia {r['redundancia']*100:.2f}%)")
        print("""
  Explicación:
  Un archivo de texto plano (.txt) usa muy pocos símbolos del alfabeto de
  256 posibles (letras, espacios, signos de puntuación), y esos símbolos
  aparecen con frecuencias muy desiguales (la letra 'e' es mucho más común
  que la 'x', por ejemplo). Esa fuerte desigualdad hace que su entropía
  empírica sea baja en relación al máximo teórico de 8 bits/símbolo, y por
  lo tanto su redundancia sea alta: hay mucho margen para comprimirlo sin
  pérdida.

  Un archivo fuertemente comprimido (.zip, .rar) es justamente el resultado
  de haber explotado esa redundancia mediante algoritmos de codificación de
  fuente (Huffman, LZ77/LZMA, aritmética, etc.). Un buen compresor deja el
  archivo resultante lo más parecido posible a ruido puro: todos los bytes
  con probabilidad casi idéntica. Por eso su entropía empírica se acerca al
  máximo teórico de 8 bits/símbolo (H ≈ L, el código es casi "compacto") y
  su redundancia tiende a 0%. Intentar comprimir ese archivo .zip de nuevo
  no logra ahorro adicional relevante, precisamente porque ya no queda
  redundancia estadística que un segundo algoritmo de compresión sin
  pérdida pueda seguir explotando.
""")


if __name__ == "__main__":
    main()

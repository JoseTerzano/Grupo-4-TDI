import struct
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "comun"))
from entropia_utils import (resumen_entropia, graficar_histograma_comparativo,
                             imprimir_resumen)


# =====================================================================
# a) Carga y validación
# =====================================================================
def validar_extension(path: str, extension_esperada: str) -> bool:
    return path.lower().endswith(extension_esperada)


def validar_formato_bmp(path: str) -> bool:
    """Un BMP válido comienza con la firma ASCII 'BM'."""
    with open(path, "rb") as f:
        firma = f.read(2)
    return firma == b"BM"


def validar_formato_jpg(path: str) -> bool:
    """Un JPG válido comienza con el marcador SOI: bytes 0xFF 0xD8."""
    with open(path, "rb") as f:
        firma = f.read(2)
    return firma == b"\xFF\xD8"


# =====================================================================
# b) Análisis de cabecera BMP (primeros 54 bytes: 14 + 40)
# =====================================================================
def leer_cabecera_bmp(path: str) -> dict:
    with open(path, "rb") as f:
        cab = f.read(54)

    if len(cab) < 54:
        raise ValueError("Cabecera BMP incompleta (archivo corrupto o truncado)")

    signature, file_size, reserved, data_offset = struct.unpack("<2sIII", cab[0:14])
    (size_info, width, height, planes, bit_count, compression,
     image_size, x_ppm, y_ppm, colors_used, colors_important) = struct.unpack(
        "<IiiHHIIiiII", cab[14:54])

    return {
        "Signature": signature.decode("ascii", errors="replace"),
        "FileSize": file_size,
        "DataOffset": data_offset,
        "Width": width,
        "Height": height,
        "Planes": planes,
        "BitCount": bit_count,
        "Compression": compression,
        "ImageSize": image_size,
    }


def imprimir_cabecera_bmp(info: dict) -> None:
    print("--- Cabecera BMP ---")
    print(f"  Signature (debe ser 'BM')  : {info['Signature']}")
    print(f"  FileSize                   : {info['FileSize']} bytes")
    print(f"  DataOffset                 : {info['DataOffset']}")
    print(f"  Ancho x Alto                : {info['Width']} x {info['Height']} px")
    print(f"  Planes (debe ser 1)         : {info['Planes']}")
    print(f"  Profundidad de color        : {info['BitCount']} bits/píxel")
    print(f"  Compresión (0 = sin comp.)  : {info['Compression']}")


# =====================================================================
# main
# =====================================================================
def main():
    if len(sys.argv) == 3:
        ruta_bmp, ruta_jpg = sys.argv[1], sys.argv[2]
    else:
        ruta_bmp = input("Ingrese la ruta del archivo .bmp: ").strip()
        ruta_jpg = input("Ingrese la ruta del archivo .jpg: ").strip()

    print("\n=== a) Validación de archivos ===")
    if not validar_extension(ruta_bmp, ".bmp") or not validar_formato_bmp(ruta_bmp):
        print(f"[ERROR] '{ruta_bmp}' no es un archivo BMP válido.")
        return
    print(f"[OK] '{ruta_bmp}' es un BMP válido (extensión + firma 'BM').")

    if not validar_extension(ruta_jpg, ".jpg") or not validar_formato_jpg(ruta_jpg):
        print(f"[ERROR] '{ruta_jpg}' no es un archivo JPG válido.")
        return
    print(f"[OK] '{ruta_jpg}' es un JPG válido (extensión + marcador SOI 0xFFD8).")

    print("\n=== b) Análisis de cabecera BMP ===")
    info_bmp = leer_cabecera_bmp(ruta_bmp)
    imprimir_cabecera_bmp(info_bmp)

    print("\n=== c) y e) Distribución de probabilidades y entropía ===")
    res_bmp = resumen_entropia(ruta_bmp)
    res_jpg = resumen_entropia(ruta_jpg)
    imprimir_resumen(res_bmp, "Archivo BMP (sin comprimir)")
    imprimir_resumen(res_jpg, "Archivo JPG (comprimido)")

    print("\n=== d) Histograma comparativo ===")
    carpeta_resultados = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultados")
    os.makedirs(carpeta_resultados, exist_ok=True)
    salida_png = os.path.join(carpeta_resultados, "histograma_bmp_vs_jpg.png")
    graficar_histograma_comparativo(
        res_bmp, res_jpg,
        titulo="Distribución de bytes: BMP (sin comprimir) vs JPG (comprimido)",
        salida_png=salida_png,
        label_a="BMP (sin comprimir)", label_b="JPG (comprimido)",
    )

    print("\n=== f) Comparación y explicación teórica ===")
    print(f"  Entropía BMP: {res_bmp['entropia_bits_simbolo']:.4f} bits/símbolo "
          f"(redundancia {res_bmp['redundancia']*100:.2f}%)")
    print(f"  Entropía JPG: {res_jpg['entropia_bits_simbolo']:.4f} bits/símbolo "
          f"(redundancia {res_jpg['redundancia']*100:.2f}%)")
    print("""
  Explicación:
  El BMP almacena el valor de CADA píxel de forma directa, sin compresión.
  Las fotografías reales tienen fuerte "redundancia espacial": píxeles
  vecinos suelen tener colores muy parecidos (el cielo, una pared, la piel,
  etc. varían suavemente). Esto hace que ciertos valores de byte se repitan
  mucho más que otros, generando picos marcados en el histograma y una
  entropía empírica notablemente menor al máximo teórico de 8 bits/símbolo.

  El JPG aplica una compresión con pérdida basada en la Transformada
  Discreta del Coseno (DCT) por bloques, cuantización perceptual y luego
  una codificación entrópica (Huffman) sobre los coeficientes resultantes.
  Ese proceso está diseñado específicamente para eliminar la redundancia
  espacial: el archivo resultante ya no representa píxeles individuales,
  sino coeficientes de frecuencia comprimidos, cuya distribución de bytes
  es mucho más uniforme. Por eso su histograma se aplana y su entropía
  empírica se acerca al límite teórico de 8 bits/símbolo: casi no queda
  redundancia explotable, lo cual es justamente el objetivo de cualquier
  buen algoritmo de compresión (acercar H(S) a L, el código compacto).
""")


if __name__ == "__main__":
    main()

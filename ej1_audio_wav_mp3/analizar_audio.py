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


def validar_formato_wav(path: str) -> bool:
    with open(path, "rb") as f:
        cabecera = f.read(12)
    if len(cabecera) < 12:
        return False
    return cabecera[0:4] == b"RIFF" and cabecera[8:12] == b"WAVE"


def validar_formato_mp3(path: str) -> bool:
    with open(path, "rb") as f:
        cabecera = f.read(3)
    if cabecera[:3] == b"ID3":
        return True
    if len(cabecera) >= 2 and cabecera[0] == 0xFF and (cabecera[1] & 0xE0) == 0xE0:
        return True
    return False


# =====================================================================
# b) Análisis de cabecera (manipulación de bytes) - formato WAV
# =====================================================================
def leer_cabecera_wav(path: str) -> dict:
    with open(path, "rb") as f:
        cab = f.read(44)

    if len(cab) < 44:
        raise ValueError("Cabecera WAV incompleta (archivo corrupto o truncado)")

    (chunk_id, chunk_size, formato,
     sub1_id, sub1_size, audio_format, num_channels,
     sample_rate, byte_rate, block_align, bits_per_sample,
     sub2_id, sub2_size) = struct.unpack("<4sI4s4sIHHIIHH4sI", cab)

    return {
        "ChunkID": chunk_id.decode("ascii", errors="replace"),
        "ChunkSize": chunk_size,
        "Format": formato.decode("ascii", errors="replace"),
        "Subchunk1ID": sub1_id.decode("ascii", errors="replace"),
        "Subchunk1Size": sub1_size,
        "AudioFormat": "PCM" if audio_format == 1 else f"Comprimido (código {audio_format})",
        "NumChannels": num_channels,
        "SampleRate": sample_rate,
        "ByteRate": byte_rate,
        "BlockAlign": block_align,
        "BitsPerSample": bits_per_sample,
        "Subchunk2ID": sub2_id.decode("ascii", errors="replace"),
        "Subchunk2Size": sub2_size,
    }


def imprimir_cabecera_wav(info: dict) -> None:
    print("--- Cabecera RIFF/WAVE ---")
    print(f"  ChunkID (debe ser 'RIFF')  : {info['ChunkID']}")
    print(f"  ChunkSize                  : {info['ChunkSize']} bytes")
    print(f"  Format (debe ser 'WAVE')   : {info['Format']}")
    print(f"  AudioFormat                : {info['AudioFormat']}")
    print(f"  Canales                    : {info['NumChannels']}")
    print(f"  Frecuencia de muestreo     : {info['SampleRate']} Hz")
    print(f"  Bits por muestra           : {info['BitsPerSample']}")
    print(f"  ByteRate                   : {info['ByteRate']} bytes/s")
    print(f"  Tamaño de datos (Subchunk2): {info['Subchunk2Size']} bytes")


# =====================================================================
# main
# =====================================================================
def main():
    if len(sys.argv) == 3:
        ruta_wav, ruta_mp3 = sys.argv[1], sys.argv[2]
    else:
        ruta_wav = input("Ingrese la ruta del archivo .wav: ").strip()
        ruta_mp3 = input("Ingrese la ruta del archivo .mp3: ").strip()

    print("\n=== a) Validación de archivos ===")
    if not validar_extension(ruta_wav, ".wav") or not validar_formato_wav(ruta_wav):
        print(f"[ERROR] '{ruta_wav}' no es un archivo WAV válido.")
        return
    print(f"[OK] '{ruta_wav}' es un WAV válido (extensión + firma RIFF/WAVE).")

    if not validar_extension(ruta_mp3, ".mp3") or not validar_formato_mp3(ruta_mp3):
        print(f"[ERROR] '{ruta_mp3}' no es un archivo MP3 válido.")
        return
    print(f"[OK] '{ruta_mp3}' es un MP3 válido (extensión + firma ID3/frame-sync).")

    print("\n=== b) Análisis de cabecera WAV ===")
    info_wav = leer_cabecera_wav(ruta_wav)
    imprimir_cabecera_wav(info_wav)

    print("\n=== c) y e) Distribución de probabilidades y entropía ===")
    res_wav = resumen_entropia(ruta_wav)
    res_mp3 = resumen_entropia(ruta_mp3)
    imprimir_resumen(res_wav, "Archivo WAV (sin comprimir)")
    imprimir_resumen(res_mp3, "Archivo MP3 (comprimido)")

    print("\n=== d) Histograma comparativo ===")
    carpeta_resultados = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultados")
    os.makedirs(carpeta_resultados, exist_ok=True)
    salida_png = os.path.join(carpeta_resultados, "histograma_wav_vs_mp3.png")
    graficar_histograma_comparativo(
        res_wav, res_mp3,
        titulo="Distribución de bytes: WAV (PCM) vs MP3 (comprimido)",
        salida_png=salida_png,
        label_a="WAV (sin comprimir)", label_b="MP3 (comprimido)",
    )

    print("\n=== f) Comparación y explicación teórica ===")
    print(f"  Entropía WAV: {res_wav['entropia_bits_simbolo']:.4f} bits/símbolo "
          f"(redundancia {res_wav['redundancia']*100:.2f}%)")
    print(f"  Entropía MP3: {res_mp3['entropia_bits_simbolo']:.4f} bits/símbolo "
          f"(redundancia {res_mp3['redundancia']*100:.2f}%)")
    print("""
  Explicación:
  El WAV (PCM) almacena cada muestra de audio "cruda", sin ningún tipo de
  compresión. Como las señales de audio reales tienen fuerte correlación
  entre muestras consecutivas (la amplitud cambia suavemente), los valores
  de byte NO son equiprobables: hay una redundancia estadística importante,
  por lo que su entropía empírica suele quedar notablemente por debajo del
  máximo teórico de 8 bits/símbolo.

  Forma del histograma WAV: con PCM de 16 bits, cada muestra es un entero
  CON SIGNO guardado en 2 bytes (little-endian: byte bajo + byte alto). La
  mayoría de las muestras tienen amplitud chica, cercana a 0:
    - muestras positivas pequeñas -> byte alto = 0x00 (valor 0)
    - muestras negativas pequeñas -> byte alto = 0xFF (valor 255, por
      complemento a 2)
  Por eso el histograma muestra DOS PICOS en los extremos (0 y 255) en
  lugar de una campana: la mitad de los bytes (los altos) se concentra en
  esos dos valores. Los bytes bajos, en cambio, se reparten de forma más
  pareja y forman la "meseta" del medio. Esa concentración en pocos valores
  es justamente la redundancia que baja la entropía.

  El MP3, en cambio, ya fue sometido a un algoritmo de compresión (con
  pérdida, basado en percepción psicoacústica + codificación entrópica tipo
  Huffman) que justamente busca eliminar esa redundancia. El resultado es
  un flujo de bytes que se aproxima mucho a una fuente aleatoria uniforme:
  su entropía empírica se acerca al máximo teórico de 8 bits/símbolo y su
  histograma se ve mucho más plano/uniforme. Esto es consistente con el
  Teorema de Codificación de Shannon: cuanto más eficiente es la
  compresión, más se acerca la longitud promedio de codificación (y por
  ende la distribución de bytes resultante) a la entropía de la fuente,
  no quedando margen para comprimir aún más sin pérdida adicional.
""")


if __name__ == "__main__":
    main()

import socket
import struct
import random
import math

HOST = "127.0.0.1"
PUERTO = 5555


# =====================================================================
# Protocolo de comunicación (mismo framing de 4 bytes que el servidor)
# =====================================================================
def recibir_exactamente(sock, cantidad):
    datos = bytearray()
    while len(datos) < cantidad:
        bloque = sock.recv(cantidad - len(datos))
        if not bloque:
            raise ConnectionError("Conexión cerrada por el servidor.")
        datos.extend(bloque)
    return bytes(datos)


def recibir_mensaje(sock):
    encabezado = recibir_exactamente(sock, 4)
    longitud = struct.unpack("!I", encabezado)[0]
    datos = recibir_exactamente(sock, longitud)
    return datos.decode("ascii")


def enviar_mensaje(sock, mensaje):
    datos = mensaje.encode("ascii")
    encabezado = struct.pack("!I", len(datos))
    sock.sendall(encabezado + datos)


# =====================================================================
# FASE 1 - Transmisión y Tasa de Error Empírica (BER)
# =====================================================================
def generar_trama_aleatoria(n_bits: int, rng: random.Random) -> str:
    return "".join(rng.choice("01") for _ in range(n_bits))


def enviar_y_medir_ber(sock, trama: str) -> dict:
    enviar_mensaje(sock, trama)
    recibida = recibir_mensaje(sock)

    errores = sum(1 for a, b in zip(trama, recibida) if a != b)
    ber = errores / len(trama)
    return {"n_bits": len(trama), "errores": errores, "ber": ber,
            "enviada": trama, "recibida": recibida}


def fase1_medir_ber(sock) -> float:
    print("=" * 60)
    print("FASE 1: Transmisión y Tasa de Error Empírica (BER)")
    print("=" * 60)

    rng = random.Random(12345)  # semilla del cliente, solo para reproducibilidad local
    tamanios = [100, 10_000, 1_000_000]
    resultados = []

    for n in tamanios:
        trama = generar_trama_aleatoria(n, rng)
        r = enviar_y_medir_ber(sock, trama)
        resultados.append(r)
        print(f"  Trama de {n:>9,} bits  ->  errores: {r['errores']:>7,}  "
              f"->  BER empírico = {r['ber']:.6f}")

    print("""
  Análisis de convergencia (Ley de los Grandes Números):
  A medida que aumenta la longitud de la trama enviada, el BER empírico
  (una frecuencia relativa de error, calculada sobre una muestra finita)
  converge hacia el valor real y fijo de la probabilidad de error "p" del
  canal. Con tramas cortas (100 bits) el BER puede oscilar bastante
  respecto del valor real, por simple variabilidad estadística de la
  muestra; con tramas largas (1.000.000 de bits) esa variabilidad se
  reduce enormemente y el BER empírico se estabiliza, aproximándose con
  alta precisión al verdadero "p" oculto en el servidor.
""")

    # Usamos la estimación de mayor tamaño de muestra (más precisa) como
    # "p teórico" para la Fase 2.
    p_estimado = resultados[-1]["ber"]
    print(f"  >> Estimación final de p (usando la muestra más grande): "
          f"{p_estimado:.6f}\n")

    # Punto 5: enviar una frase de texto, pasarla por el canal, y mostrar
    # el efecto visual del ruido.
    print("  Efecto visual del ruido sobre un mensaje de texto:")
    frase = "Teoria de la Informacion"
    binario = "".join(format(ord(c), "08b") for c in frase)
    r_frase = enviar_y_medir_ber(sock, binario)
    binario_recibido = r_frase["recibida"]

    # Reconstruir texto a partir del binario recibido (agrupando de a 8 bits)
    caracteres = []
    for i in range(0, len(binario_recibido) - 7, 8):
        byte_str = binario_recibido[i:i + 8]
        valor = int(byte_str, 2)
        caracteres.append(chr(valor) if 32 <= valor < 127 else "▯")
    texto_recuperado = "".join(caracteres)

    print(f'    Mensaje original : "{frase}"')
    print(f'    Mensaje recibido : "{texto_recuperado}"  '
          f"({r_frase['errores']} bits alterados de {r_frase['n_bits']})")

    return p_estimado


# =====================================================================
# FASE 2 - Modelado Matemático y Capacidad del Canal
# =====================================================================
def log2(x: float) -> float:
    return math.log2(x) if x > 0 else 0.0


def h_binaria(p: float) -> float:
    """Función de entropía binaria H(p) = -p*log2(p) - (1-p)*log2(1-p)."""
    if p <= 0 or p >= 1:
        return 0.0
    return -p * log2(p) - (1 - p) * log2(1 - p)


def fase2_modelado_teorico(p_estimado: float, trama_enviada: str) -> None:
    print("=" * 60)
    print("FASE 2: Modelado Matemático y Capacidad del Canal")
    print("=" * 60)

    p = p_estimado

    # 1. Matriz del canal P(Y|X), asumiendo BSC perfecto con la p estimada
    print("\n1) Matriz del Canal P(yj|xi):")
    print(f"        Y=0      Y=1")
    print(f"  X=0 | {1-p:.4f}  {p:.4f}")
    print(f"  X=1 | {p:.4f}  {1-p:.4f}")

    # 2. Probabilidades de la fuente: frecuencia relativa de 0s y 1s
    #    en la trama que efectivamente se envió.
    n = len(trama_enviada)
    n_unos = trama_enviada.count("1")
    n_ceros = n - n_unos
    p_x0 = n_ceros / n
    p_x1 = n_unos / n
    print(f"\n2) Probabilidades de la fuente (trama enviada, N={n} bits):")
    print(f"   P(X=0) = {p_x0:.4f}   P(X=1) = {p_x1:.4f}")

    # 3. Información Mutua I(X;Y) de esta transmisión específica
    h_x = -(p_x0 * log2(p_x0) if p_x0 > 0 else 0) - (p_x1 * log2(p_x1) if p_x1 > 0 else 0)
    h_p = h_binaria(p)
    # H(Y|X) = H(p) (independiente de P(X), por ser canal simétrico)
    h_y_dado_x = h_p
    # P(Y=0) = P(X=0)(1-p) + P(X=1)p ; P(Y=1) = 1 - P(Y=0)
    p_y0 = p_x0 * (1 - p) + p_x1 * p
    p_y1 = 1 - p_y0
    h_y = -(p_y0 * log2(p_y0) if p_y0 > 0 else 0) - (p_y1 * log2(p_y1) if p_y1 > 0 else 0)
    i_xy = h_y - h_y_dado_x

    print(f"\n3) Información Mutua de esta transmisión:")
    print(f"   H(X) = {h_x:.4f} bits   H(Y) = {h_y:.4f} bits   "
          f"H(Y|X) = H(p) = {h_y_dado_x:.4f} bits")
    print(f"   I(X;Y) = H(Y) - H(Y|X) = {i_xy:.4f} bits")

    # 4. Capacidad del Canal
    capacidad = 1 - h_p
    print(f"\n4) Capacidad del Canal:")
    print(f"   C = 1 - H(p) = 1 - {h_p:.4f} = {capacidad:.4f} bits/símbolo")

    # 5. Análisis de maximización
    print(f"\n5) Análisis de Maximización:")
    margen = abs(i_xy - capacidad)
    margen_relativo = margen / capacidad if capacidad > 0 else float("inf")
    print(f"   I(X;Y) obtenido = {i_xy:.4f} bits  vs  Capacidad C = {capacidad:.4f} bits")
    print(f"   Diferencia relativa = {margen_relativo*100:.2f}%")

    if margen_relativo <= 0.10:
        print("   -> El mensaje SÍ logra maximizar (aprox.) la capacidad del canal,")
        print("      dentro del margen de error aceptado (5-10%).")
    else:
        print("   -> El mensaje NO logra maximizar la capacidad del canal.")
        print("      Para que I(X;Y) sea igual a C, la trama de bits enviada")
        print("      debería tener una distribución de símbolos EQUIPROBABLE")
        print("      (P(X=0) = P(X=1) = 0.5), ya que en un BSC la capacidad se")
        print("      alcanza siempre con entrada uniforme. Si la trama enviada")
        print("      tiene más ceros que unos (o viceversa), H(X) < 1 bit y por")
        print("      lo tanto I(X;Y) queda por debajo de la capacidad máxima C.")


# =====================================================================
# main
# =====================================================================
def main():
    print(f"Conectando a {HOST}:{PUERTO} ...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PUERTO))
    print("Conectado.\n")

    try:
        p_estimado = fase1_medir_ber(sock)

        # Para la Fase 2 generamos una trama nueva (equiprobable a propósito,
        # como pide el análisis del punto 5) y la reenviamos para tener,
        # además del texto, una muestra "controlada" de fuente equiprobable
        # con la que ilustrar el caso I(X;Y) = C.
        rng = random.Random(999)
        trama_control = generar_trama_aleatoria(200_000, rng)
        enviar_mensaje(sock, trama_control)
        _ = recibir_mensaje(sock)  # se descarta; solo se usa la trama ENVIADA

        fase2_modelado_teorico(p_estimado, trama_control)
    finally:
        enviar_mensaje(sock, "SALIR")
        sock.close()
        print("\nConexión cerrada.")


if __name__ == "__main__":
    main()

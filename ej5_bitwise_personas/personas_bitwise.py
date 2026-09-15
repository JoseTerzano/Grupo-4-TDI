import json
import os
import random
import struct

# ---------------------------------------------------------------------
# Los 8 campos booleanos que se empaquetan en 1 solo byte.
# Bit 0 = LSB -> estudios_primarios ... Bit 7 = MSB -> tiene_hijos
# ---------------------------------------------------------------------
CAMPOS_BOOLEANOS = [
    "estudios_primarios",
    "estudios_secundarios",
    "estudios_universitarios",
    "vivienda_propia",
    "obra_social",
    "trabaja",
    "posee_vehiculo",
    "tiene_hijos",
]

# Longitudes fijas (en bytes) para el registro binario de longitud fija.
LEN_APELLIDO_NOMBRE = 40   # bytes, rellenado con espacios / truncado
LEN_DIRECCION = 60
LEN_DNI = 8                # DNI como entero de 8 bytes (unsigned long long)
FORMATO_STRUCT = f"<{LEN_APELLIDO_NOMBRE}s{LEN_DIRECCION}sQB"
# < : little-endian ; s: cadenas de longitud fija ; Q: DNI (8 bytes) ; B: 1 byte de flags
TAMANIO_REGISTRO_FIJO = struct.calcsize(FORMATO_STRUCT)


# =====================================================================
# Generación de datos de ejemplo (20 personas)
# =====================================================================
def generar_personas_ejemplo(cantidad: int = 20) -> list:
    random.seed(2026)
    apellidos = ["Gómez", "Pérez", "Rodríguez", "Fernández", "López", "Díaz",
                 "Martínez", "Sosa", "Romero", "Torres"]
    nombres = ["Juan", "María", "Carlos", "Ana", "Luis", "Sofía", "Diego",
               "Lucía", "Martín", "Valentina"]
    personas = []
    for i in range(cantidad):
        persona = {
            "apellido_nombre": f"{random.choice(apellidos)}, {random.choice(nombres)}",
            "direccion": f"Calle Falsa {random.randint(1,9999)}, San Juan",
            "dni": random.randint(20_000_000, 45_000_000),
        }
        for campo in CAMPOS_BOOLEANOS:
            persona[campo] = random.choice([True, False])
        personas.append(persona)
    return personas


# =====================================================================
# a) Almacenamiento en texto de longitud variable (JSON)
# =====================================================================
def guardar_json(personas: list, path: str) -> None:
    # Los booleanos se guardan como cadenas de texto "True"/"False",
    # tal como pide la consigna.
    datos = []
    for p in personas:
        d = dict(p)
        for campo in CAMPOS_BOOLEANOS:
            d[campo] = "True" if p[campo] else "False"
        datos.append(d)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)


def leer_json(path: str) -> list:
    with open(path, "r", encoding="utf-8") as f:
        datos = json.load(f)
    for d in datos:
        for campo in CAMPOS_BOOLEANOS:
            d[campo] = (d[campo] == "True")
    return datos


# =====================================================================
# b) Almacenamiento binario de longitud fija con empaquetado bitwise
# =====================================================================
def empaquetar_flags(persona: dict) -> int:
    """Empaqueta los 8 booleanos en un único byte usando operadores bitwise."""
    byte_flags = 0
    for bit_pos, campo in enumerate(CAMPOS_BOOLEANOS):
        if persona[campo]:
            byte_flags |= (1 << bit_pos)   # OR bitwise: prende el bit correspondiente
    return byte_flags


def desempaquetar_flags(byte_flags: int) -> dict:
    """Operación inversa: extrae cada booleano probando cada bit con AND bitwise."""
    resultado = {}
    for bit_pos, campo in enumerate(CAMPOS_BOOLEANOS):
        resultado[campo] = bool(byte_flags & (1 << bit_pos))
    return resultado


def guardar_binario(personas: list, path: str) -> None:
    with open(path, "wb") as f:
        for p in personas:
            apellido_nombre = p["apellido_nombre"].encode("utf-8")[:LEN_APELLIDO_NOMBRE]
            apellido_nombre = apellido_nombre.ljust(LEN_APELLIDO_NOMBRE, b" ")
            direccion = p["direccion"].encode("utf-8")[:LEN_DIRECCION]
            direccion = direccion.ljust(LEN_DIRECCION, b" ")
            dni = p["dni"]
            flags = empaquetar_flags(p)
            f.write(struct.pack(FORMATO_STRUCT, apellido_nombre, direccion, dni, flags))


def leer_binario(path: str) -> list:
    personas = []
    with open(path, "rb") as f:
        while True:
            bloque = f.read(TAMANIO_REGISTRO_FIJO)
            if not bloque:
                break
            apellido_nombre, direccion, dni, flags = struct.unpack(FORMATO_STRUCT, bloque)
            persona = {
                "apellido_nombre": apellido_nombre.decode("utf-8").rstrip(),
                "direccion": direccion.decode("utf-8").rstrip(),
                "dni": dni,
            }
            persona.update(desempaquetar_flags(flags))
            personas.append(persona)
    return personas


# =====================================================================
# main
# =====================================================================
def imprimir_persona(p: dict, idx: int) -> None:
    flags_str = ", ".join(f"{c}={'Sí' if p[c] else 'No'}" for c in CAMPOS_BOOLEANOS)
    print(f"  [{idx:02d}] {p['apellido_nombre']:<30} DNI {p['dni']}  | {p['direccion']}")
    print(f"        {flags_str}")


def main():
    carpeta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultados")
    os.makedirs(carpeta, exist_ok=True)
    ruta_json = os.path.join(carpeta, "personas_variable.json")
    ruta_bin = os.path.join(carpeta, "personas_fijo.bin")

    personas = generar_personas_ejemplo(20)

    print("=== a) Guardando en archivo de texto de longitud VARIABLE (JSON) ===")
    guardar_json(personas, ruta_json)
    print(f"[OK] Guardado en {ruta_json}")

    print("\n=== b) Guardando en archivo binario de longitud FIJA (bitwise) ===")
    guardar_binario(personas, ruta_bin)
    print(f"[OK] Guardado en {ruta_bin}")
    print(f"     Tamaño de cada registro fijo: {TAMANIO_REGISTRO_FIJO} bytes "
          f"({LEN_APELLIDO_NOMBRE} + {LEN_DIRECCION} + {LEN_DNI} + 1 byte de flags)")

    print("\n=== c) Comparación de tamaños en disco ===")
    tam_json = os.path.getsize(ruta_json)
    tam_bin = os.path.getsize(ruta_bin)
    print(f"  personas_variable.json : {tam_json} bytes")
    print(f"  personas_fijo.bin      : {tam_bin} bytes")
    print(f"  Ahorro                 : {tam_json - tam_bin} bytes "
          f"({(1 - tam_bin/tam_json)*100:.1f}% más chico el binario)")
    print("""
  Conclusión teórica:
  El formato JSON es human-readable pero muy ineficiente en bits: cada
  booleano ocupa 4-5 caracteres ("True"/"False", 32-40 bits) para
  representar 1 solo bit real de información, además de comillas, comas,
  llaves y nombres de campo repetidos en cada registro. El formato binario
  de longitud fija, en cambio, aplica el principio de "usar exactamente la
  cantidad de bits necesaria para representar la información": como cada
  campo booleano solo puede tomar 2 estados, 1 bit alcanza y sobra para
  codificarlo (log2(2) = 1 bit de entropía máxima), por lo que empaquetar
  los 8 campos en 1 solo byte (en vez de 8 bytes o 32+ bytes de texto) es
  óptimo desde el punto de vista de la Teoría de la Información. En
  sistemas de alta escala (millones de registros), esta diferencia se
  traduce directamente en menor uso de disco, menor ancho de banda de red
  y mayor velocidad de lectura/escritura.
""")

    print("=== d) Lectura y recuperación de ambos archivos ===")
    print("\n--- Registros recuperados desde JSON (texto variable) ---")
    personas_json = leer_json(ruta_json)
    for i, p in enumerate(personas_json[:3], start=1):
        imprimir_persona(p, i)
    print(f"  ... ({len(personas_json)} personas leídas en total)")

    print("\n--- Registros recuperados desde binario (fijo + bitwise) ---")
    personas_bin = leer_binario(ruta_bin)
    for i, p in enumerate(personas_bin[:3], start=1):
        imprimir_persona(p, i)
    print(f"  ... ({len(personas_bin)} personas leídas en total)")

    # Verificación de integridad: ambos formatos deben reconstruir los mismos datos
    ok = all(
        (a["apellido_nombre"] == b["apellido_nombre"] and a["direccion"] == b["direccion"]
         and a["dni"] == b["dni"] and all(a[c] == b[c] for c in CAMPOS_BOOLEANOS))
        for a, b in zip(personas_json, personas_bin)
    )
    print(f"\n[Verificación] Ambos formatos reconstruyen los mismos datos: "
          f"{'OK ✓' if ok else 'FALLÓ ✗'}")


if __name__ == "__main__":
    main()

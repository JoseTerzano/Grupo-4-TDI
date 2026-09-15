MULTIPLICADORES = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]


def calcular_digito_verificador(primeros_10_digitos: str) -> int:
    if len(primeros_10_digitos) != 10 or not primeros_10_digitos.isdigit():
        raise ValueError("Se requieren exactamente 10 dígitos numéricos.")

    suma = sum(int(d) * m for d, m in zip(primeros_10_digitos, MULTIPLICADORES))
    resto = suma % 11

    if resto == 0:
        return 0
    elif resto == 1:
        # Caso especial / CUIT teóricamente inválido para ese prefijo.
        return 9
    else:
        return 11 - resto


def validar_cuit(cuit: str) -> dict:

    cuit_limpio = cuit.replace("-", "").replace(" ", "")

    if len(cuit_limpio) != 11 or not cuit_limpio.isdigit():
        return {
            "valido": False,
            "motivo": f"Formato incorrecto: se esperaban 11 dígitos, se "
                      f"recibieron {len(cuit_limpio)} caracteres.",
        }

    primeros_10 = cuit_limpio[:10]
    digito_ingresado = int(cuit_limpio[10])
    digito_esperado = calcular_digito_verificador(primeros_10)

    return {
        "valido": digito_esperado == digito_ingresado,
        "cuit": cuit_limpio,
        "primeros_10": primeros_10,
        "digito_ingresado": digito_ingresado,
        "digito_esperado": digito_esperado,
    }


def imprimir_resultado(resultado: dict) -> None:
    if "motivo" in resultado:
        print(f"  Resultado: INVÁLIDO  ->  {resultado['motivo']}")
        return

    print(f"  CUIT ingresado        : {resultado['cuit']}")
    print(f"  Primeros 10 dígitos   : {resultado['primeros_10']}")
    print(f"  Dígito verificador esperado : {resultado['digito_esperado']}")
    print(f"  Dígito verificador ingresado: {resultado['digito_ingresado']}")
    if resultado["valido"]:
        print("  Resultado: VÁLIDO ✓")
    else:
        print("  Resultado: INVÁLIDO ✗ (el dígito de control no coincide;")
        print("             probablemente hay un error de tipeo en el número)")


# =====================================================================
# main
# =====================================================================
def main():
    print("=== Validador de CUIT/CUIL (Módulo 11) ===")
    print("(formato: 11 dígitos, con o sin guiones, ej: 20-12345678-3)\n")
    entrada = input("Ingrese el CUIT/CUIL a validar: ").strip()
    resultado = validar_cuit(entrada)
    imprimir_resultado(resultado)

    print("\n--- Ejemplos de autotest (además del ingresado por teclado) ---")
    print("(el dígito verificador se calcula con la función del programa,")
    print(" para garantizar ejemplos matemáticamente correctos)\n")
    prefijos = ["2012345678", "2730111222", "2005536943"]
    for prefijo in prefijos:
        dv_correcto = calcular_digito_verificador(prefijo)
        cuit_valido = prefijo + str(dv_correcto)
        cuit_con_error = prefijo + str((dv_correcto + 1) % 10)  # dígito adulterado

        print(f"CUIT válido       : {cuit_valido}")
        imprimir_resultado(validar_cuit(cuit_valido))
        print(f"\nMismo CUIT con dígito de control adulterado: {cuit_con_error}")
        imprimir_resultado(validar_cuit(cuit_con_error))
        print()


if __name__ == "__main__":
    main()

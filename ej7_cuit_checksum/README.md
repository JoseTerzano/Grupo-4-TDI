# Ejercicio 7 — Checksum CUIT/CUIL (Módulo 11)

Script: `cuit_checksum.py`

## Qué hace

1. Pide un CUIT/CUIL (11 dígitos, con o sin guiones).
2. Multiplica primeros 10 dígitos por `[5,4,3,2,7,6,5,4,3,2]`, suma, `resto = suma % 11`.
3. Dígito esperado: `11 - resto` (`resto 0 → 0`, `resto 1 → 9`).
4. Compara con dígito 11 → `VÁLIDO ✓` / `INVÁLIDO ✗`.
5. Autotest: 3 CUIT generados válidos + versión con dígito adulterado.

## Dependencias

- Python 3.8+
- **Sin librerías externas.**

## Cómo probar

```bash
python ej7_cuit_checksum/cuit_checksum.py
```

Casos a ingresar:

| Entrada | Esperado |
|---|---|
| `20-12345678-6` | VÁLIDO (verificado) |
| `20-12345678-5` | INVÁLIDO (dígito incorrecto) |
| `2012345678` | INVÁLIDO (formato: 10 dígitos) |
| Tu propio CUIT | VÁLIDO |

Sin interacción (PowerShell):

```powershell
"20-12345678-6" | python ej7_cuit_checksum/cuit_checksum.py
```

## Punto crítico

Caso `resto == 1` devuelve **9** siempre. Regla real AFIP: el prefijo cambia a **23** y dígito es **9** (hombres, prefijo 20) o **4** (mujeres, prefijo 27). Validar CUIT real con prefijo 23 funciona igual (algoritmo se aplica sobre prefijo ya cambiado), pero `calcular_digito_verificador("27…")` con resto 1 da resultado no real. Mencionarlo en informe o implementar la regla.

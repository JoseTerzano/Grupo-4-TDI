# Ejercicio 5 — Empaquetado bitwise: JSON vs binario fijo

Script: `personas_bitwise.py`

## Qué hace

1. Genera 20 personas de ejemplo (semilla fija `2026` → siempre mismos datos).
2. **a)** Guarda `personas_variable.json`: texto variable, booleanos como `"True"`/`"False"`.
3. **b)** Guarda `personas_fijo.bin`: registro fijo de **109 bytes**
   - Apellido y nombre: 40 bytes
   - Dirección: 60 bytes
   - DNI: 8 bytes (`Q`)
   - 8 booleanos en **1 byte** (`|=` para empaquetar, `&` para leer)
4. **c)** Compara tamaños en disco.
5. **d)** Lee ambos archivos y verifica que reconstruyen mismos datos.

## Dependencias

- Python 3.8+
- **Sin librerías externas.**

## Cómo probar

```bash
python ej5_bitwise_personas/personas_bitwise.py
```

### Resultado esperado

- Archivos `resultados/personas_variable.json` y `resultados/personas_fijo.bin` (se sobrescriben en cada ejecución).
- Binario 71.4 % más chico (ahorro de 5454 bytes).
- Última línea: `[Verificación] Ambos formatos reconstruyen los mismos datos: OK ✓` (probado).

Inspeccionar binario (PowerShell):

```powershell
Format-Hex ej5_bitwise_personas/resultados/personas_fijo.bin | Select-Object -First 8
```

## Limitaciones

- Truncado a 40/60 **bytes** UTF-8: nombre largo con tildes justo en el límite puede cortar un carácter multibyte → `UnicodeDecodeError` al leer. Datos de ejemplo no lo provocan.
- Relleno con espacios: espacios finales reales se pierden (`rstrip`).

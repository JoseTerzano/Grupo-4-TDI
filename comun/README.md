# comun — Utilidades compartidas de entropía

Módulo de apoyo. **No se ejecuta solo.** Lo importan los Ejercicios 1, 2, 3 y 4
(vía `sys.path.insert` a `../comun`).

## Qué contiene (`entropia_utils.py`)

| Función | Qué hace |
|---|---|
| `frecuencias_bytes(datos)` | Cuenta apariciones de cada byte (0-255) en un solo recorrido, O(N). |
| `entropia_shannon(frecs, total)` | `H = -Σ p_i·log2(p_i)` en bits/símbolo. |
| `redundancia(h, base_bits=8)` | `R = 1 - H / 8`. |
| `resumen_entropia(path)` | Lee un archivo y devuelve tamaño, frecuencias, entropía y redundancia. |
| `graficar_histograma_comparativo(...)` | Genera PNG con 2 histogramas (requiere `matplotlib`). |
| `imprimir_resumen(res)` | Imprime el resumen por consola. |

## Dependencias

- Python 3.8+.
- `matplotlib` **solo** para `graficar_histograma_comparativo` (Ej. 1 y 2):

```bash
python -m pip install matplotlib
```

## Importante

- No mover ni renombrar esta carpeta: los ejercicios la buscan en `../comun`.
- Lee el archivo completo en memoria (`f.read()`). Archivos de varios GB pueden agotar RAM.

## Prueba rápida

Desde la raíz del proyecto:

```bash
python -c "import sys; sys.path.insert(0,'comun'); from entropia_utils import *; print(entropia_shannon(frecuencias_bytes(b'aabb'), 4))"
```

Resultado esperado: `1.0`.

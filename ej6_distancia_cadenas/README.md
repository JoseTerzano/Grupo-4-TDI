# Ejercicio 6 — Distancias entre cadenas: Hamming y Levenshtein

Script: `distancias.py`

## Qué hace

- **a) Hamming:** cuenta posiciones distintas. Lanza `ValueError` si longitudes difieren.
- **b/c) Levenshtein:** mínimo de inserciones/eliminaciones/sustituciones, programación dinámica O(n·m).
- **d) Heurística `son_similares`:** normaliza (minúsculas, `strip`), calcula `similitud = 1 - dist / largo_max`, umbral 0.85.
- Demo con pares fijos (no pide datos).

## Dependencias

- Python 3.8+
- **Sin librerías externas.**

## Cómo probar

```bash
python ej6_distancia_cadenas/distancias.py
```

### Resultado esperado (verificado)

- `"Juan Perez"` vs `"Jaun Perez"` → Hamming = 2.
- `"Horacio López"` vs `"Oracio López"` → error esperado de Hamming; Levenshtein = 2.
- `"computadora"` vs `"computdora"` → 1.
- Heurística: `"Juan Perez"/"Jaun Perez"` → 80 % → **DATOS DISTINTOS**.

Probar pares propios:

```bash
python -c "import sys; sys.path.insert(0,'ej6_distancia_cadenas'); from distancias import *; print(distancia_levenshtein('kitten','sitting'), son_similares('Gonzalez','González'))"
```

Esperado: `3 (True, 0.875, 1)`.

## Observaciones críticas

- Heurística **no detecta transposición** "Juan/Jaun" como error de tipeo (80 % < 85 %). Levenshtein cuenta transposición como 2 operaciones. Alternativa: **Damerau-Levenshtein** (transposición = 1) o bajar umbral a 0.8 para cadenas cortas.
- Texto del programa dice "sustitución 'o'->'O' por may/min": en realidad sustituye `H→O` y elimina `o`. Resultado (2) correcto; explicación imprecisa.
- Levenshtein usa matriz completa: memoria O(n·m). Para cadenas largas usar 2 filas.

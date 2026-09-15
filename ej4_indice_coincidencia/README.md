# Ejercicio 4 — Índice de Coincidencia (IC)

Script: `indice_coincidencia.py`

## Qué hace

- Calcula `IC = Σ f_i(f_i - 1) / (N(N - 1))` por archivo.
- Calcula también entropía (reutiliza `../comun`).
- Imprime ambas métricas y explica su relación inversa (más redundancia → mayor IC, menor entropía) y uso en criptoanálisis (Vigenère).

## Dependencias

- Python 3.8+
- Carpeta `../comun`.
- **Sin librerías externas.**

## Cómo probar

Usa los archivos de prueba del Ejercicio 3 (`ej3_entropia_archivos/pruebas/`), para no duplicar 3 MB. Solo imprime por consola.

```bash
python ej4_indice_coincidencia/indice_coincidencia.py ej3_entropia_archivos/pruebas/quijote.txt ej3_entropia_archivos/pruebas/quijote.zip
```

Modo interactivo:

```bash
python ej4_indice_coincidencia/indice_coincidencia.py
```

### Resultado esperado

- `.txt`: IC alto (≈ 0.06–0.09), entropía baja.
- `.zip` grande: IC cercano a `1/256 ≈ 0.0039`, entropía ≈ 8.
- Verificado con Quijote: TXT → IC bytes 0.0658 / IC letras 0.0745; ZIP → IC bytes 0.00391 / IC letras 0.0385.

## Dos IC por archivo

El script muestra dos valores:

| Métrica | Alfabeto | Referencia |
|---|---|---|
| **IC (bytes)** | 256 valores de byte crudos | Aleatorio ≈ 1/256 = 0.0039 |
| **IC (letras)** | 27 letras A-Z + Ñ (mayúsculas, sin tildes, sin espacios ni puntuación) | Español ≈ 0.074 · Aleatorio ≈ 1/27 = 0.037 |

Solo el IC por letras es comparable con 0.074. El IC por bytes queda más bajo porque espacios y puntuación reparten la probabilidad.

Verificado con Don Quijote (Gutenberg #2000): IC letras ≈ 0.0745.

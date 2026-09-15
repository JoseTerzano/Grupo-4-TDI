# Ejercicio 8 — Capacidad de canal 2x4 por búsqueda exhaustiva

Script: `capacidad_canal.py`

## Qué hace

1. **a)** Pide matriz `P(Y|X)` 2 filas × 4 columnas (valida: 4 valores, entre 0 y 1, fila suma 1). O usa matriz de ejemplo.
2. **b-d)** Barre `P(X=0)` de 0.00 a 1.00, paso 0.01 (101 puntos). En cada uno:
   - `P(Y)` por probabilidad total.
   - `I(X;Y) = H(Y) - H(Y|X)`.
3. **e)** Muestra máximo: capacidad `C`, `P(X)` óptima, `P(Y)`, `H(Y)`, `H(Y|X)`.

## Dependencias

- Python 3.8+
- **Sin librerías externas.**

## Cómo probar

```bash
python ej8_capacidad_canal/capacidad_canal.py
```

### Caso 1 — ejemplo (responder `n`)

Esperado (verificado):
```
Capacidad del Canal C = 0.554498 bits/símbolo
Lograda con P(X=0) = 0.50
```
Matriz simétrica → óptimo en 0.5. Correcto.

### Caso 2 — canal perfecto (responder `s`)

```
Fila X=0: 1 0 0 0
Fila X=1: 0 0 0 1
```
Esperado: `C = 1.000000`, `P(X=0) = 0.50`.

### Caso 3 — canal inútil

```
Fila X=0: 0.25 0.25 0.25 0.25
Fila X=1: 0.25 0.25 0.25 0.25
```
Esperado: `C = 0.000000`.

### Caso 4 — asimétrico (verifica que óptimo ≠ 0.5)

```
Fila X=0: 1 0 0 0
Fila X=1: 0.5 0.5 0 0
```
Esperado: `C ≈ 0.3219`, `P(X=0) ≈ 0.60`.

## Limitaciones

- Precisión limitada al paso 0.01: `C` real puede diferir levemente. Para más precisión, llamar `buscar_capacidad_canal(matriz, paso=0.0001)` o usar algoritmo de Blahut-Arimoto.
- Validación de suma usa tolerancia `1e-6`: ingresar `0.333 0.333 0.334 0` funciona; `1/3` como texto no.

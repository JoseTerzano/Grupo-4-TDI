# Ejercicio 3 — Entropía empírica: texto vs comprimido

Script: `entropia_archivo.py`

## Qué hace

- Lee **cualquier archivo** en un recorrido O(N).
- Calcula entropía de Shannon (bits/símbolo), redundancia respecto de 8 bits y símbolos únicos.
- Con 2+ archivos: imprime comparación y explicación (texto redundante vs comprimido ≈ ruido).

## Dependencias

- Python 3.8+
- Carpeta `../comun`.
- **No requiere librerías externas.**

## Cómo probar

### Estructura

```
ej3_entropia_archivos/
├── entropia_archivo.py
└── pruebas/
    ├── quijote.txt   <- Don Quijote, Gutenberg #2000, texto plano UTF-8 (2.2 MB)
    └── quijote.zip   <- mismo archivo comprimido (Compress-Archive, 819 KB)
```

Estos archivos también los usa el **Ejercicio 4**. El script solo imprime por consola (no genera archivos de resultados).

### Con los archivos incluidos

```bash
python ej3_entropia_archivos/entropia_archivo.py ej3_entropia_archivos/pruebas/quijote.txt ej3_entropia_archivos/pruebas/quijote.zip
```

Resultado verificado: TXT 4.53 bits/símbolo (redundancia 43.4 %) vs ZIP 7.999 bits/símbolo (0.01 %).

### Con archivos propios

- `texto.txt`: texto natural **grande y variado** (≥ 30 KB).
- `texto.zip`: comprimir ese mismo archivo (`Compress-Archive texto.txt texto.zip`).

```bash
python ej3_entropia_archivos/entropia_archivo.py texto.txt texto.zip
```

Modo interactivo (rutas separadas por coma):

```bash
python ej3_entropia_archivos/entropia_archivo.py
```

### Resultado esperado

| Archivo | Entropía | Redundancia |
|---|---|---|
| `.txt` natural | ~4.3–5.6 bits | 30–45 % |
| `.zip` | ~7.9+ bits | < 2 % |

## Advertencia

Texto **repetitivo** (misma frase copiada) produce ZIP diminuto (cientos de bytes) con entropía ~5 bits: muestra insuficiente, cabecera ZIP domina. Probado: 44 KB repetitivos → ZIP 358 bytes → 5.39 bits. Usar texto real.

## Limitaciones

- Rutas con coma no funcionan en modo interactivo (separador). Usar argumentos.
- Carga archivo entero en memoria.

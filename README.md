# Práctico de Máquina 1 — Teoría de la Información

Licenciatura en Ciencias de la Computación — Año 2026

Este repositorio contiene la resolución de los 9 ejercicios de programación
del Práctico de Máquina 1. Cada ejercicio está en su propia carpeta, con su
script principal y un `README.md` que explica qué hace, qué necesita y cómo
probarlo.

## Estructura

```
practico_maquina1/
├── README.md
├── requirements.txt               <- dependencias externas (matplotlib, Pillow)
├── .gitignore / .gitattributes
├── comun/
│   ├── entropia_utils.py          <- funciones compartidas (entropía, frecuencias,
│   │                                  histogramas), reutilizadas por Ej. 1, 2, 3 y 4
│   └── README.md
├── ej1_audio_wav_mp3/
│   ├── analizar_audio.py          <- Ejercicio 1: Entropía en audio WAV vs MP3
│   ├── pruebas/                   <- Ring05.wav, Ring05Nuevo.mp3
│   └── resultados/                <- histograma_wav_vs_mp3.png
├── ej2_imagen_bmp_jpg/
│   ├── analizar_imagen.py         <- Ejercicio 2: Entropía en imágenes BMP vs JPG
│   ├── pruebas/                   <- prueba.jpg (prueba.bmp se regenera, ver su README)
│   └── resultados/                <- histograma_bmp_vs_jpg.png
├── ej3_entropia_archivos/
│   ├── entropia_archivo.py        <- Ejercicio 3: Entropía empírica (texto vs comprimido)
│   └── pruebas/                   <- quijote.txt, quijote.zip (también los usa el Ej. 4)
├── ej4_indice_coincidencia/
│   └── indice_coincidencia.py     <- Ejercicio 4: Índice de Coincidencia (IC)
├── ej5_bitwise_personas/
│   ├── personas_bitwise.py        <- Ejercicio 5: Empaquetado bitwise (JSON vs binario fijo)
│   └── resultados/                <- personas_variable.json, personas_fijo.bin
├── ej6_distancia_cadenas/
│   └── distancias.py              <- Ejercicio 6: Distancia de Hamming y Levenshtein
├── ej7_cuit_checksum/
│   └── cuit_checksum.py           <- Ejercicio 7: Checksum CUIT/CUIL (Módulo 11)
├── ej8_capacidad_canal/
│   └── capacidad_canal.py         <- Ejercicio 8: Capacidad de canal por búsqueda exhaustiva
└── ej9_bsc_sockets/
    ├── servidor_bsc.py            <- Ejercicio 9: Servidor BSC (provisto por la cátedra)
    └── cliente_bsc.py             <- Ejercicio 9: Cliente (Fase 1 + Fase 2)
```

Cada carpeta `ejN_*` tiene además su propio `README.md`.

- `pruebas/`: archivos de entrada usados para verificar (Ej. 1, 2 y 3; el Ej. 4 reutiliza los del Ej. 3).
- `resultados/`: archivos que generan los scripts (histogramas del Ej. 1 y 2, JSON/binario del Ej. 5). Se sobrescriben en cada ejecución.

## Requisitos

| Dependencia | Versión | Usada en | Para qué |
|---|---|---|---|
| Python | 3.8 o superior (probado con 3.13) | Todos | — |
| `matplotlib` | ≥ 3.5 (probado con 3.11.2) | Ej. 1 y 2 | Generar los histogramas |
| `Pillow` | ≥ 9.0 (probado con 12.3.0) | Ej. 2 | Regenerar `prueba.bmp`, que no está en el repositorio (27.6 MB) |

Los Ejercicios 3 a 9 usan solo la librería estándar (`math`, `struct`,
`collections`, `json`, `random`, `socket`, `threading`, etc.).

Instalar todo desde la raíz del proyecto:

```bash
python -m pip install -r requirements.txt
```

`matplotlib` instala automáticamente sus propias dependencias (`numpy`,
`contourpy`, `fonttools`, etc.).

Usar `python -m pip` en lugar de `pip` evita el error `Fatal error in launcher`
cuando `pip.exe` quedó apuntando a una instalación de Python borrada.

Todos los comandos se ejecutan **desde la raíz del proyecto**. Los scripts que
leen archivos (Ej. 1, 2, 3, 4) aceptan las rutas como argumentos o las piden
por teclado:

```bash
python ej3_entropia_archivos/entropia_archivo.py ej3_entropia_archivos/pruebas/quijote.txt ej3_entropia_archivos/pruebas/quijote.zip
```

## Resumen de cada ejercicio y resultados verificados

**Ej. 1 — Audio WAV vs MP3.** Valida ambos archivos (firma RIFF/WAVE para
WAV, ID3/frame-sync para MP3), desempaqueta la cabecera WAV de 44 bytes con
`struct`, calcula la entropía empírica byte a byte y genera un histograma
comparativo. Probado con un sonido de Windows (`Ring05.wav`) y el mismo audio
exportado a MP3 con Audacity: **6.16 bits/símbolo (redundancia 23 %) vs 7.98
bits/símbolo (0.25 %)**. El histograma del WAV muestra dos picos en 0 y 255,
por el byte alto de las muestras PCM de 16 bits con signo.

**Ej. 2 — Imagen BMP vs JPG.** Misma lógica que el Ej. 1, pero desempaqueta
la cabecera BMP de 54 bytes (Bitmap File Header + Bitmap Info Header) y
valida el marcador SOI (`0xFFD8`) para JPG. Probado con un fondo de pantalla
de Windows de 3840×2400 guardado en ambos formatos: **BMP 7.55 bits/símbolo
(27.6 MB) vs JPG 7.80 bits/símbolo (467 KB)**.

**Ej. 3 — Entropía empírica genérica.** Lee cualquier archivo en un solo
recorrido O(N) y calcula su entropía y redundancia respecto del máximo
teórico de 8 bits/símbolo. Probado con *Don Quijote* (Proyecto Gutenberg,
2.2 MB) contra su versión .zip: **4.53 bits/símbolo (43 % de redundancia) vs
7.999 bits/símbolo (0.01 %)**.

**Ej. 4 — Índice de Coincidencia.** Implementa `IC = Σf_i(f_i-1) / N(N-1)`
en dos versiones: sobre bytes crudos y sobre las 27 letras del español (sin
espacios, puntuación ni tildes). Con los archivos del Ej. 3: IC por letras del
texto **0.0745** (referencia teórica del español ≈ 0.074) e IC por bytes del
ZIP **0.00391** (= 1/256, fuente uniforme). Explica la relación inversa entre
IC y entropía.

**Ej. 5 — Empaquetado bitwise.** Genera 20 personas de ejemplo, las guarda
en JSON (booleanos como texto) y en binario de longitud fija de 109 bytes por
registro (8 booleanos empaquetados en 1 solo byte mediante `|=` y `&`),
compara tamaños en disco (**71.4 % más chico el binario**) y verifica que
ambos formatos recuperan exactamente los mismos datos.

**Ej. 6 — Distancias entre cadenas.** Implementa Hamming (con error si las
longitudes difieren) y Levenshtein por programación dinámica. Incluye una
heurística de similitud basada en distancia de edición normalizada (umbral
85 %) como propuesta de comparación aproximada.

**Ej. 7 — Checksum CUIT/CUIL.** Implementa el algoritmo de Módulo 11,
valida un CUIT ingresado por teclado y corre autotests con CUITs válidos y
versiones adulteradas para demostrar la detección de errores.

**Ej. 8 — Capacidad de canal (2x4) por fuerza bruta.** Pide la matriz
`P(Y|X)` (o usa una de ejemplo), barre `P(X=0)` de 0.00 a 1.00 en pasos de
0.01, calcula `I(X;Y)` en cada paso y se queda con el máximo. Con la matriz
simétrica de ejemplo: **C = 0.5545 bits/símbolo en `P(X=0) = 0.50`**, como
predice la teoría. Probado también con canal perfecto (C = 1), inútil (C = 0)
y asimétrico (óptimo en `P(X=0) = 0.60`).

**Ej. 9 — BSC sobre sockets TCP.** `servidor_bsc.py` es el código provisto
por la cátedra. `cliente_bsc.py` implementa la Fase 1 (mide el BER empírico
con tramas de 100 / 10.000 / 1.000.000 de bits y muestra el efecto del ruido
sobre un mensaje de texto) y la Fase 2 (arma la matriz del canal, calcula
`I(X;Y)` y la capacidad `C = 1 - H(p)` con la `p` estimada, y analiza si el
mensaje maximiza la capacidad). Probado de punta a punta: la `p` estimada
(**0.060868**) coincide casi exactamente con la `p` real oculta en el
servidor (**0.060968**), y `C = 0.6691 bits/símbolo`.

Para correr el Ejercicio 9 hacen falta dos terminales:

```bash
# Terminal 1
python ej9_bsc_sockets/servidor_bsc.py

# Terminal 2 (una vez que el servidor esté escuchando)
python ej9_bsc_sockets/cliente_bsc.py
```

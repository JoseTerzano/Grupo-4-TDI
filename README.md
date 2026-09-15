# Práctico de Máquina 1 — Teoría de la Información

Licenciatura en Ciencias de la Computación — Año 2026

Este repositorio contiene la resolución de los 9 ejercicios de programación
del Práctico de Máquina 1. Cada ejercicio está en su propia carpeta, con un
único script principal, autocontenido y comentado.

## Estructura

```
practico_maquina1/
├── comun/
│   └── entropia_utils.py          <- funciones compartidas (entropía, frecuencias,
│                                      histogramas), reutilizadas por Ej. 1, 2, 3 y 4
├── ej1_audio_wav_mp3/
│   └── analizar_audio.py          <- Ejercicio 1: Entropía en audio WAV vs MP3
├── ej2_imagen_bmp_jpg/
│   └── analizar_imagen.py         <- Ejercicio 2: Entropía en imágenes BMP vs JPG
├── ej3_entropia_archivos/
│   └── entropia_archivo.py        <- Ejercicio 3: Entropía empírica genérica (texto vs comprimido)
├── ej4_indice_coincidencia/
│   └── indice_coincidencia.py     <- Ejercicio 4: Índice de Coincidencia (IC)
├── ej5_bitwise_personas/
│   └── personas_bitwise.py        <- Ejercicio 5: Empaquetado bitwise (JSON vs binario fijo)
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

### Subcarpetas por ejercicio

- `pruebas/`: archivos de entrada usados para verificar (Ej. 1, 2 y 3; el Ej. 4 reutiliza los del Ej. 3).
- `resultados/`: archivos que generan los scripts (histogramas del Ej. 1 y 2, JSON/binario del Ej. 5). Se sobrescriben en cada ejecución.

## Requisitos

- Python 3.8 o superior (sin dependencias externas para la mayoría de los
  ejercicios: usan solo la librería estándar).
- **Ejercicios 1 y 2** necesitan `matplotlib` para generar los histogramas:
  ```
  python -m pip install matplotlib
  ```
- No se requiere ninguna librería adicional para probar la lógica de los
  Ejercicios 1 y 2 con imágenes/audios reales: solo `matplotlib`. (Para
  *generar* archivos de prueba .bmp/.jpg uno mismo, `Pillow` es útil pero
  no es necesario para ejecutar los programas, que leen archivos ya
  existentes.)

Todos los scripts que leen archivos (Ej. 1, 2, 3, 4) funcionan tanto en
modo **interactivo** (piden la ruta por teclado) como pasando las rutas
como **argumentos de línea de comandos**, útil para pruebas automáticas:

```bash
python ej3_entropia_archivos/entropia_archivo.py miarchivo.txt miarchivo.zip
```

## Resumen de cada ejercicio y cómo se resolvió

**Ej. 1 — Audio WAV vs MP3.** Valida ambos archivos (firma RIFF/WAVE para
WAV, ID3/frame-sync para MP3), desempaqueta la cabecera WAV de 44 bytes con
`struct`, calcula la entropía empírica byte a byte de cada archivo y genera
un histograma comparativo. Probado con un WAV sintético (tono senoidal) y
un "MP3" con datos pseudoaleatorios: **6.23 bits/símbolo vs 7.99
bits/símbolo**, exactamente el comportamiento esperado.

**Ej. 2 — Imagen BMP vs JPG.** Misma lógica que el Ej. 1, pero desempaqueta
la cabecera BMP de 54 bytes (Bitmap File Header + Bitmap Info Header) y
valida el marcador SOI (`0xFFD8`) para JPG. Probado con una imagen generada
con Pillow guardada en ambos formatos.

**Ej. 3 — Entropía empírica genérica.** Lee cualquier archivo en un solo
recorrido O(N) y calcula su entropía y redundancia respecto del máximo
teórico de 8 bits/símbolo. Probado con un texto en español natural (46 KB)
contra su versión .zip: **5.56 bits/símbolo (30% de redundancia) vs 7.98
bits/símbolo (0.2% de redundancia)** — confirma la teoría perfectamente.

**Ej. 4 — Índice de Coincidencia.** Implementa `IC = Σf_i(f_i-1) / N(N-1)`
reutilizando el módulo común, y lo compara con la entropía de los mismos
archivos del Ej. 3, explicando la relación inversa entre ambas métricas.

**Ej. 5 — Empaquetado bitwise.** Genera 20 personas de ejemplo, las guarda
en JSON (booleanos como texto) y en binario de longitud fija (8 booleanos
empaquetados en 1 solo byte mediante `|=` y `&` bitwise), compara tamaños
en disco (**70% más chico el binario** en la prueba realizada) y verifica
que ambos formatos recuperan exactamente los mismos datos.

**Ej. 6 — Distancias entre cadenas.** Implementa Hamming (con detección de
error si las longitudes difieren) y Levenshtein por programación dinámica.
Incluye una heurística de similitud basada en distancia de edición
normalizada como propuesta de comparación aproximada.

**Ej. 7 — Checksum CUIT/CUIL.** Implementa el algoritmo de Módulo 11
completo, valida un CUIT ingresado por teclado y corre autotests generando
CUITs válidos (y versiones adulteradas) para demostrar la detección de
errores.

**Ej. 8 — Capacidad de canal (2x4) por fuerza bruta.** Pide la matriz
`P(Y|X)` (o usa una de ejemplo), barre `P(X=0)` de 0.00 a 1.00 en pasos de
0.01, calcula `I(X;Y)` en cada paso y se queda con el máximo. Probado con
una matriz simétrica de ejemplo: la capacidad se alcanza correctamente en
`P(X=0) = 0.50`, como predice la teoría.

**Ej. 9 — BSC sobre sockets TCP.** `servidor_bsc.py` es el código provisto
por la cátedra sin modificaciones. `cliente_bsc.py` implementa la Fase 1
(mide el BER empírico con tramas de 100 / 10.000 / 1.000.000 de bits, y
muestra el efecto del ruido sobre un mensaje de texto) y la Fase 2 (arma la
matriz del canal, calcula `I(X;Y)` y la Capacidad `C = 1 - H(p)` usando la
`p` estimada en la Fase 1, y analiza si el mensaje enviado maximiza la
capacidad). **Probado de punta a punta**, levantando servidor y cliente
juntos: la `p` estimada empíricamente (0.060868) coincidió casi
exactamente con la `p` real oculta en el servidor (0.060968), y con una
trama equiprobable de control se verificó que `I(X;Y) = C` con 0.00% de
diferencia, tal como predice la teoría del BSC.

Para correr el Ejercicio 9 hacen falta dos terminales:

```bash
# Terminal 1
python ej9_bsc_sockets/servidor_bsc.py

# Terminal 2 (una vez que el servidor esté escuchando)
python ej9_bsc_sockets/cliente_bsc.py
```

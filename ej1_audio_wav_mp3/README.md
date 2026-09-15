# Ejercicio 1 — Entropía en audio: WAV vs MP3

Script: `analizar_audio.py`

## Qué hace

1. **Valida** ambos archivos: extensión + firma interna
   - WAV: `RIFF` en offset 0 y `WAVE` en offset 8.
   - MP3: tag `ID3` o frame-sync MPEG (`0xFF 0xE?`).
2. **Desempaqueta la cabecera WAV** (44 bytes) con `struct`: canales, frecuencia de muestreo, bits por muestra, etc.
3. **Calcula entropía y redundancia** byte a byte de cada archivo (usa `../comun/entropia_utils.py`).
4. **Genera histograma comparativo** `resultados/histograma_wav_vs_mp3.png`.
5. Imprime explicación teórica.

## Dependencias

- Python 3.8+
- **`matplotlib` (obligatorio)** — sin él, el script falla en el paso d) con `ModuleNotFoundError`.

```bash
python -m pip install -r requirements.txt
```

(Desde la raíz del proyecto. Instala `matplotlib` y `Pillow`; este ejercicio solo necesita `matplotlib`.)

Usar `python -m pip`, no `pip` solo: evita el error `Fatal error in launcher` cuando `pip.exe` apunta a un Python desinstalado.

- Carpeta `../comun` presente.
- Un archivo `.wav` y un `.mp3` (incluidos en `pruebas/`).

## Estructura

```
ej1_audio_wav_mp3/
├── analizar_audio.py
├── pruebas/
│   ├── Ring05.wav         <- C:\Windows\Media\Ring05.wav
│   └── Ring05Nuevo.mp3    <- mismo WAV exportado a MP3 con Audacity
└── resultados/
    └── histograma_wav_vs_mp3.png   <- se regenera en cada ejecución
```

## Cómo probar

Desde la raíz del proyecto, con los archivos incluidos:

```bash
python ej1_audio_wav_mp3/analizar_audio.py ej1_audio_wav_mp3/pruebas/Ring05.wav ej1_audio_wav_mp3/pruebas/Ring05Nuevo.mp3
```

Resultado verificado: WAV 6.16 bits/símbolo (redundancia 22.98 %) vs MP3 7.98 bits/símbolo (0.25 %).

Con archivos propios:

```bash
python ej1_audio_wav_mp3/analizar_audio.py ruta/audio.wav ruta/audio.mp3
```

O sin argumentos (pide rutas por teclado):

```bash
python ej1_audio_wav_mp3/analizar_audio.py
```

### Resultado esperado

- `[OK]` en ambas validaciones.
- Cabecera WAV legible. Con `Ring05.wav`: `RIFF`, `WAVE`, `PCM`, 2 canales, 22050 Hz, 16 bits.
- Entropía MP3 ≈ 7.9+ bits/símbolo; WAV menor.
- PNG generado en `resultados/`. El WAV muestra dos picos en 0 y 255: byte alto de muestras PCM de 16 bits con signo cercanas a cero (positivas → `0x00`, negativas → `0xFF`).

**Recomendación:** usar la misma canción en ambos formatos (convertir con Audacity o ffmpeg) para comparación justa.

## Limitaciones conocidas

- Asume cabecera WAV **canónica de 44 bytes**. WAV con chunks extra (`LIST`, `fact`, WAV exportados por algunos editores) muestran `Subchunk2ID` y `Subchunk2Size` incorrectos. Entropía no se ve afectada. `Ring05.wav` tiene 152 bytes extra al final (probablemente metadatos): no altera el resultado.
- Extensión en mayúsculas funciona (`.WAV`); `.wave` no.
- Tonos sintéticos puros dan entropía WAV alta (~7.5); audio real muestra mejor la diferencia.

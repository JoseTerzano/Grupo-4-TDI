# Ejercicio 2 — Entropía en imágenes: BMP vs JPG

Script: `analizar_imagen.py`

## Qué hace

1. **Valida** ambos archivos: extensión + firma
   - BMP: bytes `BM`.
   - JPG: marcador SOI `0xFF 0xD8`.
2. **Desempaqueta cabecera BMP** (54 bytes: File Header 14 + Info Header 40): tamaño, ancho, alto, bits/píxel, compresión.
3. **Calcula entropía y redundancia** de ambos (usa `../comun`).
4. **Genera histograma** `resultados/histograma_bmp_vs_jpg.png`.
5. Imprime explicación teórica.

## Dependencias

- Python 3.8+
- **`matplotlib` (obligatorio)** y **`Pillow`** (para regenerar el BMP). Ambos están en `requirements.txt`:

```bash
python -m pip install -r requirements.txt
```

Usar `python -m pip`, no `pip` solo: evita el error `Fatal error in launcher` cuando `pip.exe` apunta a un Python desinstalado.

- Carpeta `../comun` presente.
- Un `.bmp` y un `.jpg`: `prueba.jpg` está incluido; `prueba.bmp` se regenera (ver abajo).

## Estructura

```
ej2_imagen_bmp_jpg/
├── analizar_imagen.py
├── pruebas/
│   ├── prueba.bmp   <- NO incluido en el repo (27.6 MB); se regenera desde prueba.jpg
│   └── prueba.jpg   <- 3840x2400, desde C:\Windows\Web\Wallpaper\Windows\img0.jpg, calidad 85
└── resultados/
    └── histograma_bmp_vs_jpg.png   <- se regenera en cada ejecución
```

## Cómo probar

### Con los archivos incluidos

`prueba.bmp` **no está en el repositorio** (27.6 MB, excluido en `.gitignore`). Regenerarlo antes de ejecutar:

```bash
python -c "from PIL import Image; Image.open('ej2_imagen_bmp_jpg/pruebas/prueba.jpg').convert('RGB').save('ej2_imagen_bmp_jpg/pruebas/prueba.bmp')"
```

Luego ejecutar:

```bash
python ej2_imagen_bmp_jpg/analizar_imagen.py ej2_imagen_bmp_jpg/pruebas/prueba.bmp ej2_imagen_bmp_jpg/pruebas/prueba.jpg
```

Resultado verificado:

| Archivo | Tamaño | Entropía |
|---|---|---|
| BMP original (desde el JPG de Windows) | 27.6 MB | 7.546 bits/símbolo |
| BMP regenerado (desde `prueba.jpg`) | 27.6 MB | 7.558 bits/símbolo |
| JPG | 467 KB | 7.804 bits/símbolo |

La pequeña diferencia entre ambos BMP se debe a que el regenerado parte del JPG ya comprimido. La conclusión no cambia.

### Con una foto propia

```bash
python -c "from PIL import Image; im=Image.open('foto.jpg').convert('RGB'); im.save('ej2_imagen_bmp_jpg/pruebas/prueba.bmp'); im.save('ej2_imagen_bmp_jpg/pruebas/prueba.jpg', quality=85)"
```

### Resultado esperado

- `[OK]` en validaciones.
- Cabecera: `BM`, dimensiones correctas, 24 bits/píxel, compresión 0.
- Con **foto real**: JPG ≈ 7.8–7.97 bits/símbolo; BMP menor.
- PNG generado en `resultados/`.

## Limitaciones conocidas

- Solo acepta extensión `.jpg`. **`.jpeg` es rechazado** aunque sea válido. Renombrar o ajustar `validar_extension`.
- Imágenes sintéticas pequeñas (degradados) pueden dar resultado **invertido** (JPG con menor entropía), por peso de tablas de cabecera JPG. Usar fotos reales de varios cientos de KB.
- Cabecera asume `BITMAPINFOHEADER` (40 bytes). BMP V4/V5 leen campos base bien, pero ignoran el resto.

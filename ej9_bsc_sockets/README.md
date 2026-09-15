# Ejercicio 9 — Canal Binario Simétrico (BSC) sobre sockets TCP

Scripts:
- `servidor_bsc.py` — provisto por cátedra. Simula canal ruidoso con `p` oculta. **No modificar.**
- `cliente_bsc.py` — solución: Fase 1 + Fase 2.

## Qué hace

### Servidor
- Escucha en `0.0.0.0:5555`.
- Protocolo: 4 bytes de longitud (big-endian) + mensaje ASCII de `0`/`1`.
- Invierte cada bit con probabilidad `p` (derivada de semilla 2026). Devuelve trama alterada.
- Mensaje `SALIR` cierra sesión. Un hilo por cliente; ruido determinista por sesión.

### Cliente
- **Fase 1:** envía tramas aleatorias de 100, 10.000 y 1.000.000 bits → mide BER. Toma BER de 1M como `p` estimada. Envía frase "Teoria de la Informacion" en binario y muestra texto corrupto.
- **Fase 2:** con `p` estimada arma matriz BSC, calcula `H(X)`, `H(Y)`, `H(Y|X)=H(p)`, `I(X;Y)`, capacidad `C = 1 - H(p)`, y compara `I(X;Y)` vs `C` usando trama equiprobable de 200.000 bits.

## Dependencias

- Python 3.8+
- **Sin librerías externas** (`socket`, `struct`, `threading`).
- Puerto **5555** libre.
- Firewall de Windows puede preguntar al iniciar servidor: permitir red privada (o cancelar: cliente local usa `127.0.0.1` igual).

## Cómo probar

Requiere **2 terminales** en la raíz del proyecto.

**Terminal 1 — servidor:**
```bash
python ej9_bsc_sockets/servidor_bsc.py
```
Esperar: `Escuchando en puerto 5555`.

**Terminal 2 — cliente:**
```bash
python ej9_bsc_sockets/cliente_bsc.py
```

### Resultado esperado (verificado en esta PC)

```
Trama de       100 bits -> BER empírico = 0.060000
Trama de    10,000 bits -> BER empírico = 0.060400
Trama de 1,000,000 bits -> BER empírico = 0.060868
Mensaje recibido : "teOrka de▯lk Infosmac▯o."  (10 bits alterados de 192)
C = 1 - H(p) = 0.6691 bits/símbolo
Diferencia relativa = 0.00%
Conexión cerrada.
```

Resultados idénticos en cada ejecución (semillas fijas). Detener servidor con `Ctrl+C`.

## Problemas comunes

| Error | Causa / solución |
|---|---|
| `ConnectionRefusedError` | Servidor no iniciado. Arrancar Terminal 1 primero. |
| `OSError: [WinError 10048]` | Puerto 5555 ocupado (servidor previo abierto). Cerrarlo. |
| Caracteres raros `▯` | Consola sin UTF-8. Ejecutar `chcp 65001` o usar Windows Terminal. |
| Tarda varios segundos | Normal: servidor procesa 1M bits en bucle Python. |

## Observación crítica

"Diferencia 0.00 %" es **tautológica**: `I(X;Y)` y `C` se calculan con misma `p` teórica y entrada casi exactamente 0.5/0.5, por lo que coinciden por construcción. No mide el canal real. Para análisis más fuerte: calcular `I(X;Y)` **empírica** a partir de la matriz de conteos (enviado vs recibido) de la trama de control.

# 🕰️ Reloj Analógico Creativo con Números Romanos

Este es un reloj analógico interactivo y visualmente atractivo creado en Python con `tkinter`. Utiliza listas circulares dobles para modelar el funcionamiento interno de las manecillas del reloj, incluyendo el segundero, minutero y horero. Además, reproduce un sonido tipo "tick" cada segundo y adapta visualmente su apariencia según la hora del día.

---

## 🚀 Características

- ⏱️ Reloj completamente funcional con manecillas animadas.
- 🔢 Números romanos representando las horas.
- 🔄 Diseño circular y elegante con animación pulsante en el centro.
- 🎨 Cambios de color de fondo según el momento del día:
  - Mañana: 🌅
  - Tarde: 🌇
  - Noche: 🌃
- 🔊 Sonido "tick" por segundo (requiere archivo `tick.wav`).
- 📅 Ventana tipo casilla que muestra el día del mes dentro del reloj.

---

## 📁 Archivos importantes

- `main.py`: interfaz gráfica del reloj.
- `clock_logic.py`: lógica del reloj con listas circulares dobles.
- `tick.wav`: sonido que se reproduce cada segundo (opcional).
- `README.md`: este archivo.

---

## ▶️ Ejecución

Asegúrate de tener Python 3 instalado y ejecuta:

```bash
python main.py

📌 Requisitos
Python 3.x

Módulos estándar: tkinter, math, datetime, threading, os

Librería adicional: pytz
Instala con:

bash
Copiar
Editar
pip install pytz

Desarrollado por Juan David Maya Benavides
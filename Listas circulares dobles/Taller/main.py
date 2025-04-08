
import tkinter as tk
import math
import threading
import os
from clock_logic import Clock
from datetime import datetime
import pytz
import winsound  # Solo en Windows, si usas Linux te doy la versión para eso

WIDTH = 400
HEIGHT = 400
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2
RADIUS = 150

class AnalogClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Clock")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
        self.canvas.pack()

        self.clock = Clock()
        self.tick_sound = True  # Puedes cambiar a False si no quieres sonido
        self.center_pulse = 0

        self.update_clock()

    def get_background_color(self):
        colombia_time = datetime.now(pytz.timezone("America/Bogota"))
        hour = colombia_time.hour
        if 6 <= hour < 12:
            return "#FFFAE3"  # Mañana
        elif 12 <= hour < 18:
            return "#FFE4B5"  # Tarde
        else:
            return "#2C3E50"  # Noche

    def draw_minute_marks(self):
        for i in range(60):
            angle = math.radians(i * 6 - 90)
            inner = RADIUS - 8 if i % 5 == 0 else RADIUS - 4
            outer = RADIUS - 2
            x1 = CENTER_X + inner * math.cos(angle)
            y1 = CENTER_Y + inner * math.sin(angle)
            x2 = CENTER_X + outer * math.cos(angle)
            y2 = CENTER_Y + outer * math.sin(angle)
            self.canvas.create_line(x1, y1, x2, y2, fill="black", width=1)

    def play_tick_sound(self):
        if self.tick_sound and os.path.exists("tick.wav"):
            threading.Thread(target=lambda: winsound.PlaySound("tick.wav", winsound.SND_FILENAME)).start()

    def draw_clock_face(self):
        self.canvas.delete("all")
        bg_color = self.get_background_color()
        self.canvas.configure(bg=bg_color)

        # Círculo con aspecto tipo metálico/madera (simulado)
        for r in range(RADIUS, RADIUS - 20, -1):
            color = f"#{r % 256:02x}{100 + r % 100:02x}{100:02x}"
            self.canvas.create_oval(CENTER_X - r, CENTER_Y - r,
                                    CENTER_X + r, CENTER_Y + r,
                                    outline=color)

        # Marcadores de minutos
        self.draw_minute_marks()

        # Números romanos
        for i, numeral in enumerate(self.clock.roman_hours):
            angle = math.radians(i * 30 - 60)
            x = CENTER_X + (RADIUS - 30) * math.cos(angle)
            y = CENTER_Y + (RADIUS - 30) * math.sin(angle)
            self.canvas.create_text(x, y, text=numeral, font=("Orbitron", 16, "bold"), fill="black")

        # Ventana de la fecha (día del mes)
        colombia_time = datetime.now(pytz.timezone("America/Bogota"))
        day = colombia_time.strftime("%d")
        date_x = CENTER_X + 60
        date_y = CENTER_Y

        self.canvas.create_rectangle(date_x - 20, date_y - 15,
                                     date_x + 20, date_y + 15,
                                     fill="white", outline="black", width=2)
        self.canvas.create_text(date_x, date_y, text=day,
                                font=("Courier", 14, "bold"), fill="black")

    def draw_hand(self, length, angle_deg, color, width=3):
        angle_rad = math.radians(angle_deg - 90)
        x = CENTER_X + length * math.cos(angle_rad)
        y = CENTER_Y + length * math.sin(angle_rad)
        self.canvas.create_line(CENTER_X, CENTER_Y, x, y, fill=color, width=width)

    def animate_center_pulse(self):
        pulse = 5 + self.center_pulse
        self.center_pulse = (self.center_pulse + 1) % 4
        return pulse

    def update_clock(self):
        self.draw_clock_face()

        hour_node = self.clock.get_hour_pointer()
        minute_node = self.clock.get_minute_pointer()
        second = self.clock.get_second_pointer()

        real_hour = self.clock.get_hour_value()
        hour_angle = (real_hour % 12) * 30 + (minute_node.value / 60) * 30
        minute_angle = minute_node.value * 6
        second_angle = second * 6

        self.draw_hand(RADIUS * 0.5, hour_angle, "black", width=5)
        self.draw_hand(RADIUS * 0.8, minute_angle, "blue", width=3)
        self.draw_hand(RADIUS * 0.9, second_angle, "red", width=1)

        # Centro animado
        pulse = self.animate_center_pulse()
        self.canvas.create_oval(CENTER_X - pulse, CENTER_Y - pulse,
                                CENTER_X + pulse, CENTER_Y + pulse,
                                fill="black", outline="white")

        # Sonido
        self.play_tick_sound()

        self.root.after(1000, self.update_clock)

if __name__ == "__main__":
    root = tk.Tk()
    app = AnalogClockApp(root)
    root.mainloop()

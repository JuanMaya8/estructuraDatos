# clock_logic.py

from doubly_circular_list import DoublyCircularList, HourNode, MinuteNode
from datetime import datetime
from pytz import timezone
import pytz

class Clock:
    def __init__(self):
        self.hours = DoublyCircularList()
        self.minutes = DoublyCircularList()

        self.roman_hours = ['I', 'II', 'III', 'IV', 'V', 'VI',
                            'VII', 'VIII', 'IX', 'X', 'XI', 'XII']

        for h in self.roman_hours:
            self.hours.append(h, node_type=HourNode)

        for m in range(60):
            self.minutes.append(m, node_type=MinuteNode)

    def get_current_time(self):
        # Hora exacta de Colombia
        colombia = timezone('America/Bogota')
        now = datetime.now(colombia)
        hour_24 = now.hour
        hour_12 = hour_24 % 12
        hour_12 = 12 if hour_12 == 0 else hour_12
        minute = now.minute
        return hour_12, minute

    def get_hour_pointer(self):
        hour, _ = self.get_current_time()
        return self.hours.find(self.roman_hours[hour - 1])

    def get_minute_pointer(self):
        _, minute = self.get_current_time()
        return self.minutes.find(minute)

    def get_second_pointer(self):
        colombia = timezone('America/Bogota')
        now = datetime.now(colombia)
        return now.second
    
    def get_hour_value(self):
        colombia_time = datetime.now(pytz.timezone('America/Bogota'))
        hour_24 = colombia_time.hour
        hour_12 = hour_24 % 12
        return 12 if hour_12 == 0 else hour_12


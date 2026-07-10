from machine import Pin
import time


class Input:

    def __init__(self):

        self.up = Pin(7, Pin.IN, Pin.PULL_UP)
        self.down = Pin(8, Pin.IN, Pin.PULL_UP)
        self.select = Pin(9, Pin.IN, Pin.PULL_UP)

        self.last_up = 1
        self.last_down = 1
        self.last_select = 1

        self.last_time = time.ticks_ms()

        self.debounce = 150


    def update(self):

        now = time.ticks_ms()

        if time.ticks_diff(now, self.last_time) < self.debounce:
            return None


        # UP
        value = self.up.value()

        if value == 0 and self.last_up == 1:
            self.last_up = value
            self.last_time = now
            return "UP"

        self.last_up = value


        # DOWN
        value = self.down.value()

        if value == 0 and self.last_down == 1:
            self.last_down = value
            self.last_time = now
            return "DOWN"

        self.last_down = value


        # SELECT
        value = self.select.value()

        if value == 0 and self.last_select == 1:
            self.last_select = value
            self.last_time = now
            return "SELECT"

        self.last_select = value


        return None
import config
import time

class Keyer:
    def __init__(self, audio):
        self.audio = audio
        self.buffer = ""
        self.last = time.ticks_ms()

    def dit(self):
        self.audio.beep(config.UNIT)
        self.buffer += "."
        self.last = time.ticks_ms()

    def dah(self):
        self.audio.beep(config.UNIT * 3)
        self.buffer += "-"
        self.last = time.ticks_ms()

    def ready_to_decode(self):
        return time.ticks_diff(time.ticks_ms(), self.last) > 1200
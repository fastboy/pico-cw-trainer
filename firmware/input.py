from machine import Pin
import config

class Input:
    def __init__(self):
        self.dit = Pin(config.PIN_DIT, Pin.IN, Pin.PULL_UP)
        self.dah = Pin(config.PIN_DAH, Pin.IN, Pin.PULL_UP)

    def read(self):
        return {
            "dit": not self.dit.value(),
            "dah": not self.dah.value()
        }
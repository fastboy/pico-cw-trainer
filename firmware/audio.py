from machine import Pin, PWM
import config
import time

class Audio:
    def __init__(self):
        self.sp = PWM(Pin(config.PIN_AUDIO))
        self.sp.freq(config.TONE_FREQ)
        self.off()

    def on(self):
        self.sp.duty_u16(config.TONE_LEVEL)

    def off(self):
        self.sp.duty_u16(0)

    def beep(self, duration_ms):
        self.on()
        time.sleep_ms(duration_ms)
        self.off()
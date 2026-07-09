from machine import Pin, PWM


class Speaker:

    def __init__(self, pin=4, frequency=650):

        self.pwm = PWM(Pin(pin))
        self.pwm.freq(frequency)
        self.off()


    def on(self):

        self.pwm.duty_u16(30000)


    def off(self):

        self.pwm.duty_u16(0)


    def set_frequency(self, frequency):

        self.pwm.freq(frequency)
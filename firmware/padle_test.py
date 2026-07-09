from machine import Pin, PWM
import time

from keyer import Keyer


dot = Pin(2, Pin.IN, Pin.PULL_UP)
dash = Pin(3, Pin.IN, Pin.PULL_UP)


speaker = PWM(Pin(4))
speaker.freq(650)
speaker.duty_u16(0)


keyer = Keyer(wpm=12)


while True:

    # paddle state
    if not dot.value():
        keyer.hold_dot()
    else:
        keyer.release_dot()


    if not dash.value():
        keyer.hold_dash()
    else:
        keyer.release_dash()


    # keyer
    keyer.update(time.ticks_ms())


    # audio
    if keyer.output:
        speaker.duty_u16(30000)
    else:
        speaker.duty_u16(0)


    time.sleep_ms(5)
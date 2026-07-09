from machine import Pin, PWM
import time

from keyer import Keyer


# -----------------------------
# Buttons
# -----------------------------
dot = Pin(2, Pin.IN, Pin.PULL_UP)
dash = Pin(3, Pin.IN, Pin.PULL_UP)


# -----------------------------
# Speaker
# -----------------------------
speaker = PWM(Pin(4))
speaker.freq(650)
speaker.duty_u16(0)


# -----------------------------
# Keyer
# -----------------------------
keyer = Keyer(wpm=12)


print("Keyer speaker test")


while True:

    if not dot.value():
        print("DOT BUTTON")
        keyer.request_dot()

    if not dash.value():
        print("DASH BUTTON")
        keyer.request_dash()


    keyer.update(time.ticks_ms())


    print(
        "output:",
        keyer.output,
        "state:",
        keyer.state
    )


    if keyer.output:
        speaker.duty_u16(30000)
    else:
        speaker.duty_u16(0)


    time.sleep_ms(20)

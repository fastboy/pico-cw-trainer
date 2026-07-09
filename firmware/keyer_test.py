from machine import Pin
import time
from keyer import Keyer

# ------------------------
# Button pins
# ------------------------

DOT_PIN = 14
DASH_PIN = 15

dot = Pin(DOT_PIN, Pin.IN, Pin.PULL_UP)
dash = Pin(DASH_PIN, Pin.IN, Pin.PULL_UP)

# ------------------------

keyer = Keyer(12)

last_debug = time.ticks_ms()

dot_last = False
dash_last = False

while True:

    now = time.ticks_ms()

    # ------------------------
    # Dot paddle
    # ------------------------

    dot_pressed = not dot.value()

    if dot_pressed and not dot_last:

        keyer.request_dot()
        keyer.hold_dot()

    elif not dot_pressed and dot_last:

        keyer.release_dot()

    dot_last = dot_pressed

    # ------------------------
    # Dash paddle
    # ------------------------

    dash_pressed = not dash.value()

    if dash_pressed and not dash_last:

        keyer.request_dash()
        keyer.hold_dash()

    elif not dash_pressed and dash_last:

        keyer.release_dash()

    dash_last = dash_pressed

    # ------------------------

    keyer.update(now)

    if time.ticks_diff(now, last_debug) > 250:

        keyer.debug()
        last_debug = now

    time.sleep_ms(5)

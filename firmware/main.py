import time

from keyer import Keyer


keyer = Keyer(18)


start = time.ticks_ms()

pressed = False
released = False


while True:

    now = time.ticks_ms()


    if not pressed and time.ticks_diff(now, start) > 1000:

        print("DASH PADDLE DOWN")

        keyer.hold_dash()

        keyer.request_dash()

        pressed = True


    if not released and time.ticks_diff(now, start) > 5000:

        print("DASH PADDLE UP")

        keyer.release_dash()

        released = True


    keyer.update(now)

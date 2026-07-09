from machine import Pin, PWM
import time

from keyer import Keyer
from decoder import Decoder
from display import Display


# -----------------------------
# Paddle
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
# Modules
# -----------------------------
keyer = Keyer(wpm=12)
decoder = Decoder()
display = Display()


display.title()
display.show_speed(12)


print("CW Trainer test")


while True:


    # -------------------------
    # Paddle input
    # -------------------------

    if not dot.value():
        keyer.hold_dot()
    else:
        keyer.release_dot()


    if not dash.value():
        keyer.hold_dash()
    else:
        keyer.release_dash()



    # -------------------------
    # Keyer
    # -------------------------

    keyer.update(time.ticks_ms())



    # -------------------------
    # Speaker
    # -------------------------

    if keyer.output:
        speaker.duty_u16(30000)
    else:
        speaker.duty_u16(0)



    # -------------------------
    # Decoder
    # -------------------------

    if keyer.new_element == keyer.DOT:

        decoder.add_dot()
        display.show_pattern(
            decoder.buffer
        )


    elif keyer.new_element == keyer.DASH:

        decoder.add_dash()
        display.show_pattern(
            decoder.buffer
        )


    letter = decoder.update()

    if letter:

        pattern, character = letter

        display.show_letter(
            character
        )

        print(
            pattern,
            "=",
            character
        )


    time.sleep_ms(5)
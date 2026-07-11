from machine import Pin, PWM
import time

from display import Display
from menu import Menu
from settings import Settings
from input import Input

from keyer import Keyer


# -------------------------
# Hardware objects
# -------------------------

display = Display()

buttons = Input()


# -------------------------
# Menus / Screens
# -------------------------

settings = Settings(display)

menu = Menu(
    display,
    settings
)


# -------------------------
# Sound / Keyer
# -------------------------

speaker = PWM(Pin(4))
speaker.freq(650)
speaker.duty_u16(0)


keyer = Keyer(wpm=12)


dot = Pin(2, Pin.IN, Pin.PULL_UP)
dash = Pin(3, Pin.IN, Pin.PULL_UP)



# -------------------------
# Current screen
# -------------------------

screen = "menu"


current_editor = None



# -------------------------
# Start
# -------------------------

display.title()

menu.open()



# -------------------------
# Main loop
# -------------------------

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



    keyer.update(time.ticks_ms())


    # -------------------------
    # Audio output
    # -------------------------

    if keyer.output:

        speaker.duty_u16(30000)

    else:

        speaker.duty_u16(0)



    # -------------------------
    # Buttons
    # -------------------------

    event = buttons.update()



    # -------------------------
    # MENU
    # -------------------------

    if screen == "menu":


        if event == "UP":

            menu.up()


        elif event == "DOWN":

            menu.down()


        elif event == "SELECT":


            result = menu.select()


            if result == "settings":

                settings.open()

                screen = "settings"



    # -------------------------
    # SETTINGS
    # -------------------------

    elif screen == "settings":


        if event == "UP":

            settings.up()


        elif event == "DOWN":

            settings.down()


        elif event == "SELECT":


            result = settings.select()


            if result == "speed":


                current_editor = settings.speed

                current_editor.open()

                screen = "speed"



            elif result == "tone":


                current_editor = settings.tone

                current_editor.open()

                screen = "tone"



            elif result == "back":


                menu.open()

                screen = "menu"



    # -------------------------
    # SPEED EDITOR
    # -------------------------

    elif screen == "speed":


        if event:

            current_editor.update(event)



        if event == "SELECT":


            result = current_editor.confirm()


            if result == "back":


                settings.open()

                screen = "settings"



    # -------------------------
    # TONE EDITOR
    # -------------------------

    elif screen == "tone":


        if event:

            current_editor.update(event)



        if event == "SELECT":


            result = current_editor.confirm()


            if result == "back":


                settings.open()

                screen = "settings"



    time.sleep_ms(10)
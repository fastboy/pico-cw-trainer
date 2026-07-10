from display import Display
from menu import Menu
from settings import Settings
from input import Input
import time


display = Display()

settings = Settings(display)

menu = Menu(
    display,
    settings
)

buttons = Input()


# Current active screen
screen = "menu"


display.title()

menu.open()


while True:

    event = buttons.update()


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



    elif screen == "settings":

        if event == "UP":
            settings.up()

        elif event == "DOWN":
            settings.down()

        elif event == "SELECT":

            result = settings.select()


            if result == "speed":

                speed = settings.speed
                screen = "speed"


            elif result == "back":

                menu.open()
                screen = "menu"



    elif screen == "speed":

        print("SPEED SCREEN", event)

        if event:

            speed.update(event)


        if event == "SELECT":

            result = speed.confirm()


            if result == "back":

                settings.open()
                screen = "settings"


        elif event == "SELECT":

            result = speed.confirm()


            if result == "back":

                settings.open()
                screen = "settings"



    time.sleep_ms(10)
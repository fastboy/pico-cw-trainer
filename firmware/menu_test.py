from display import Display
from menu import Menu
from input import Input
import time


display = Display()

menu = Menu(display)

buttons = Input()


display.title()

menu.open()


while True:

    event = buttons.update()


    if event == "UP":
        menu.up()

    elif event == "DOWN":
        menu.down()

    elif event == "SELECT":
        menu.select()


    time.sleep_ms(10)

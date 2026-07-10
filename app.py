from machine import Pin, PWM
import time

from display import Display
from input import Input
from menu import Menu
from settings import Settings
from keyer import Keyer


class App:

    def __init__(self):

        # -------------------------
        # Display
        # -------------------------

        self.display = Display()

        # -------------------------
        # Input
        # -------------------------

        self.buttons = Input()

        # -------------------------
        # Settings / Menu
        # -------------------------

        self.settings = Settings(self.display)

        self.menu = Menu(
            self.display,
            self.settings
        )

        # -------------------------
        # Audio
        # -------------------------

        self.speaker = PWM(Pin(4))
        self.speaker.freq(650)
        self.speaker.duty_u16(0)

        # -------------------------
        # Paddle
        # -------------------------

        self.dot = Pin(2, Pin.IN, Pin.PULL_UP)
        self.dash = Pin(3, Pin.IN, Pin.PULL_UP)

        self.keyer = Keyer()

        # -------------------------
        # Current screen
        # -------------------------

        self.screen = "menu"

        self.display.title()
        self.menu.open()
        
    def update(self):

        #
        # Paddle
        #

        if not self.dot.value():
            self.keyer.hold_dot()
        else:
            self.keyer.release_dot()

        if not self.dash.value():
            self.keyer.hold_dash()
        else:
            self.keyer.release_dash()

        self.keyer.update(time.ticks_ms())

        #
        # Audio
        #

        if self.keyer.output:
            self.speaker.duty_u16(30000)
        else:
            self.speaker.duty_u16(0)

        #
        # Buttons
        #

        event = self.buttons.update()

        if self.screen == "menu":

            if event == "UP":
                self.menu.up()

            elif event == "DOWN":
                self.menu.down()

            elif event == "SELECT":

                result = self.menu.select()

                if result == "settings":

                    self.settings.open()
                    self.screen = "settings"

        elif self.screen == "settings":

            if event == "UP":
                self.settings.up()

            elif event == "DOWN":
                self.settings.down()

            elif event == "SELECT":

                result = self.settings.select()

                if result == "speed":

                    self.settings.speed.open()
                    self.screen = "speed"

                elif result == "tone":

                    self.settings.tone.open()
                    self.screen = "tone"

                elif result == "back":

                    self.menu.open()
                    self.screen = "menu"

        elif self.screen == "speed":

            if event:

                self.settings.speed.update(event)

            if event == "SELECT":

                if self.settings.speed.confirm() == "back":

                    self.settings.open()
                    self.screen = "settings"

        elif self.screen == "tone":

            if event:

                self.settings.tone.update(event)

            if event == "SELECT":

                if self.settings.tone.confirm() == "back":

                    self.settings.open()
                    self.screen = "settings"

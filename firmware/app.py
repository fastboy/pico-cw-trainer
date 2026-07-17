from machine import Pin, PWM
import time
import config

from learn import Learn
from practice import Practice
from single_character import SingleCharacter
from character_groups import CharacterGroups
from words import Words

from display import Display
from input import Input

from menu import Menu
from settings import Settings
from speed import Speed
from tone import Tone

from keyer import Keyer


class App:

    def __init__(self):

        # -------------------------
        # Hardware
        # -------------------------

        self.display = Display()

        self.buttons = Input()


        # -------------------------
        # Sound / Keyer
        # -------------------------

        self.speaker = PWM(
            Pin(4)
        )

        self.speaker.freq(
            config.SIDETONE_FREQ
        )

        self.speaker.duty_u16(0)


        self.keyer = Keyer(
            wpm=config.WPM
        )

        self.dot = Pin(
            2,
            Pin.IN,
            Pin.PULL_UP
        )

        self.dash = Pin(
            3,
            Pin.IN,
            Pin.PULL_UP
        )


        # -------------------------
        # Screens
        # -------------------------

        self.menu = Menu(
            self.display
        )

        self.settings = Settings(
            self.display
        )

        self.speed = Speed(
            self.display
        )

        self.tone = Tone(
            self.display
        )

        self.practice = Practice(
            self.display,
            self.keyer
        )
        
        self.learn = Learn(
            self.display
        )
        
        self.single_character = SingleCharacter(
            self.display,
            self.keyer
        )
        self.character_groups = CharacterGroups(
            self.display,
            self.keyer
        )
        self.words = Words(
            self.display,
            self.keyer
        )

        # -------------------------
        # Screen hierarchy
        # -------------------------

        self.settings.parent = self.menu
        self.speed.parent = self.settings
        self.tone.parent = self.settings

        self.practice.parent = self.menu
        
        self.learn.parent = self.menu
        self.single_character.parent = self.learn
        self.character_groups.parent = self.learn
        self.words.parent = self.learn
        


        # -------------------------
        # Screen registry
        # -------------------------
        #
        # Screens may currently return names such as:
        #
        #     "settings"
        #     "speed"
        #     "tone"
        #
        # The registry converts those names into screen objects.
        # Adding another screen requires only one new entry here.
        # No new elif result == "..." block is needed.
        # -------------------------

        self.screens = {
            "menu": self.menu,
            "settings": self.settings,
            "speed": self.speed,
            "tone": self.tone,
            "practice": self.practice,
            "learn": self.learn,
            "single_character": self.single_character,
            "character_groups": self.character_groups,
            "words": self.words,
        }


        # -------------------------
        # Current screen
        # -------------------------

        self.current_screen = self.menu

        # -------------------------
        # Start
        # -------------------------

        self.display.title()

        self.current_screen.open()


    def change_screen(self, screen):

        # A screen may return a registry name:
        #
        #     "settings"
        #
        # or it may return the screen object directly:
        #
        #     self.parent

        if isinstance(screen, str):

            screen = self.screens.get(
                screen
            )

        if screen is None:

            return

        self.current_screen = screen

        self.current_screen.open()


    def update(self):

        # -------------------------
        # Paddle
        # -------------------------

        if not self.dot.value():

            self.keyer.hold_dot()

        else:

            self.keyer.release_dot()


        if not self.dash.value():

            self.keyer.hold_dash()

        else:

            self.keyer.release_dash()


        self.keyer.update(
            time.ticks_ms()
        )
        
        # -------------------------
        # Keyer events
        # -------------------------

        for keyer_event in self.keyer.get_events():

            if hasattr(
                self.current_screen,
                "add_element"
            ):

                self.current_screen.add_element(

                    keyer_event,

                    self.keyer.DOT,

                    self.keyer.DASH
                )

        # -------------------------
        # Audio
        # -------------------------

        if self.keyer.output:

            self.speaker.duty_u16(
                30000
            )

        else:

            self.speaker.duty_u16(
                0
            )

        # -------------------------
        # Screen timer
        # -------------------------

        if hasattr(
            self.current_screen,
            "tick"
        ):

            self.current_screen.tick()

        # -------------------------
        # Buttons
        # -------------------------

        event = self.buttons.update()

        if event:

            result = self.current_screen.update(
                event
            )

            if result:

                self.change_screen(
                    result
                )




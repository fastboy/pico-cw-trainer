from screen import Screen
from decoder import Decoder
from morse import MORSE

import config
import random
import st7789


class SingleCharacter(Screen):

    def __init__(
        self,
        display,
        keyer
    ):

        super().__init__()

        self.display = display

        # The same keyer object used by app.py
        self.keyer = keyer

        self.parent = None

        self.decoder = Decoder(
            config.WPM
        )

        # Use letters for the first lesson
        self.characters = []

        for character in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":

            if character in MORSE:

                self.characters.append(
                    character
                )

        self.target = ""

        self.input_pattern = ""

        self.result_text = ""

        self.result_color = st7789.WHITE

        self.hint_visible = False

        self.answered = False


    # -------------------------
    # Open screen
    # -------------------------

    def open(self):

        # Apply the latest configured speed
        self.keyer.set_speed(
            config.WPM
        )

        self.decoder.set_speed(
            config.WPM
        )

        self.new_character()

        super().open()


    # -------------------------
    # Select another character
    # -------------------------

    def new_character(self):

        previous = self.target

        if not self.characters:

            self.target = "A"

        else:

            self.target = random.choice(
                self.characters
            )

            # Avoid showing the same character
            # twice in a row when possible.
            if len(self.characters) > 1:

                while self.target == previous:

                    self.target = random.choice(
                        self.characters
                    )

        self.decoder.clear()

        self.input_pattern = ""

        self.result_text = ""

        self.result_color = st7789.WHITE

        self.hint_visible = False

        self.answered = False


    # -------------------------
    # Front buttons
    # -------------------------
    #
    # SELECT = Back
    # DOWN   = Next
    # UP     = Show / Hide
    # -------------------------

    def update(self, event):

        if event == "SELECT":

            return self.parent


        elif event == "DOWN":

            self.new_character()

            self.draw()


        elif event == "UP":

            self.hint_visible = (
                not self.hint_visible
            )

            self.draw_hint()

            self.draw_softkeys()


        return None


    # -------------------------
    # Receive keyer elements
    # -------------------------

    def add_element(
        self,
        element,
        dot_value,
        dash_value
    ):

        # Once an answer has been checked,
        # NEXT starts another character.
        if self.answered:

            return


        if element == dot_value:

            self.decoder.add_dot()


        elif element == dash_value:

            self.decoder.add_dash()


        self.input_pattern = (
            self.decoder.buffer
        )

        self.draw_input()


    # -------------------------
    # Decoder timer
    # -------------------------

    def tick(self):

        result = self.decoder.update()

        if not result:

            return


        pattern, character = result

        # Ignore the later word-space event.
        if not pattern:

            return


        self.input_pattern = pattern

        expected_pattern = MORSE.get(
            self.target,
            ""
        )


        if pattern == expected_pattern:

            self.result_text = "CORRECT"

            self.result_color = (
                st7789.GREEN
            )

        else:

            self.result_text = "X WRONG"

            self.result_color = (
                st7789.RED
            )


        self.answered = True

        # Reveal the correct answer after
        # the user's attempt.
        self.hint_visible = True

        self.draw_input()

        self.draw_hint()

        self.draw_result()

        self.draw_softkeys()


        print(
            "Target:",
            self.target,
            expected_pattern,
            "Input:",
            pattern,
            self.result_text
        )


    # -------------------------
    # Draw hint
    # -------------------------

    def draw_hint(self):

        self.display.tft.fill_rect(
            190,
            68,
            120,
            25,
            st7789.BLACK
        )


        if self.hint_visible:

            pattern = MORSE.get(
                self.target,
                ""
            )

            self.display.tft.text(
                self.display.font,
                pattern,
                205,
                68,
                st7789.CYAN
            )


    # -------------------------
    # Draw user input
    # -------------------------

    def draw_input(self):

        self.display.tft.fill_rect(
            10,
            130,
            300,
            25,
            st7789.BLACK
        )

        self.display.tft.text(
            self.display.font,
            self.input_pattern,
            10,
            130,
            st7789.WHITE
        )


    # -------------------------
    # Draw result
    # -------------------------

    def draw_result(self):

        self.display.tft.fill_rect(
            105,
            168,
            205,
            25,
            st7789.BLACK
        )


        if self.result_text:

            self.display.tft.text(
                self.display.font,
                self.result_text,
                105,
                168,
                self.result_color
            )


    # -------------------------
    # Draw soft keys
    # -------------------------

    def draw_softkeys(self):

        if self.hint_visible:

            right_label = " HIDE"

        else:

            right_label = " SHOW"


        self.display.show_softkeys(
            "BACK",
            " NEXT",
            right_label
        )


    # -------------------------
    # Draw complete screen
    # -------------------------

    def draw(self):

        self.display.clear()

        self.display.title()

        self.display.show_speed(
            config.WPM
        )


        # -------------------------
        # Headings
        # -------------------------

        self.display.tft.text(
            self.display.font,
            "CHARACTER",
            10,
            42,
            st7789.YELLOW
        )

        self.display.tft.text(
            self.display.font,
            "PATTERN",
            190,
            42,
            st7789.YELLOW
        )


        # -------------------------
        # Target character
        # -------------------------

        self.display.tft.text(
            self.display.font,
            self.target,
            65,
            68,
            st7789.GREEN
        )


        # -------------------------
        # User input heading
        # -------------------------

        self.display.tft.text(
            self.display.font,
            "YOUR INPUT",
            10,
            105,
            st7789.YELLOW
        )


        # -------------------------
        # Result heading
        # -------------------------

        self.display.tft.text(
            self.display.font,
            "RESULT:",
            10,
            168,
            st7789.YELLOW
        )


        self.draw_hint()

        self.draw_input()

        self.draw_result()

        self.draw_softkeys()
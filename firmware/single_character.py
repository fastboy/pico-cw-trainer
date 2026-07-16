import theme
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

        self.keyer = keyer

        self.parent = None

        self.decoder = Decoder(
            config.WPM
        )

        # Letters and digits
        self.characters = []

        for character in (
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            "1234567890"
        ):

            if character in MORSE:

                self.characters.append(
                    character
                )

        # Current character the user should send
        self.target = ""

        # Last pattern sent by the user
        self.input_pattern = ""

        # Character represented by the pattern
        self.input_character = ""

        self.result_text = ""

        self.result_color = st7789.WHITE

        self.hint_visible = False

        self.wrong_attempts = 0


    # -------------------------
    # Open screen
    # -------------------------

    def open(self):

        self.keyer.set_speed(
            config.WPM
        )

        self.decoder.set_speed(
            config.WPM
        )

        self.select_character(
            clear_feedback=True
        )

        super().open()


    # -------------------------
    # Select random character
    # -------------------------

    def select_character(
        self,
        clear_feedback=True
    ):

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

        self.wrong_attempts = 0

        # Hide the hint for each new target.
        self.hint_visible = False

        if clear_feedback:

            self.input_pattern = ""

            self.input_character = ""

            self.result_text = ""

            self.result_color = (
                theme.TEXT
            )


    # -------------------------
    # Front buttons
    # -------------------------
    #
    # SELECT = Back
    # DOWN   = Next character
    # UP     = Show / Hide pattern
    # -------------------------

    def update(self, event):

        if event == "SELECT":

            return self.parent


        elif event == "DOWN":

            # Manually skip to another character.
            self.select_character(
                clear_feedback=True
            )

            self.draw()


        elif event == "UP":

            # Hint is always available.
            self.hint_visible = (
                not self.hint_visible
            )

            self.draw_target_area()

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

        # When the first element of a new
        # attempt arrives, remove the previous
        # answer and result.
        #
        # This lets the previous correct answer
        # remain visible while the next target
        # is already displayed.
        if not self.decoder.buffer:

            self.input_pattern = ""

            self.input_character = ""

            self.result_text = ""

            self.draw_input()

            self.draw_result()


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

        # Ignore later word-space events.
        if not pattern:

            return


        expected_pattern = MORSE.get(
            self.target,
            ""
        )

        self.input_pattern = pattern

        # Show what the transmitted pattern means.
        if character:

            self.input_character = character

        else:

            self.input_character = "?"


        # -------------------------
        # Correct answer
        # -------------------------

        if pattern == expected_pattern:

            self.result_text = "CORRECT"

            self.result_color = (
                theme.SUCCESS
            )

            print(
                "Target:",
                self.target,
                expected_pattern,
                "Input:",
                pattern,
                self.input_character,
                "CORRECT"
            )

            # Display the completed answer.
            self.draw_input()

            self.draw_result()

            # Automatically select the next target,
            # but keep the previous sent pattern,
            # decoded character and result visible.
            self.select_character(
                clear_feedback=False
            )

            self.draw_target_area()

            self.draw_softkeys()


        # -------------------------
        # Incorrect answer
        # -------------------------

        else:

            self.wrong_attempts += 1

            self.result_text = "INCORRECT"

            self.result_color = (
                theme.ERROR
            )

            # Automatically reveal the correct
            # pattern after three incorrect tries.
            if self.wrong_attempts >= 3:

                self.hint_visible = True


            print(
                "Target:",
                self.target,
                expected_pattern,
                "Input:",
                pattern,
                self.input_character,
                "INCORRECT",
                self.wrong_attempts
            )

            self.draw_input()

            self.draw_result()

            self.draw_target_area()

            self.draw_softkeys()

            # Prepare for another attempt at
            # the same character.
            self.decoder.clear()


    # -------------------------
    # Draw current target
    # -------------------------

    def draw_target_area(self):

        # Clear target character area
        self.display.tft.fill_rect(
            10,
            68,
            130,
            25,
            theme.BACKGROUND
        )

        # Clear pattern hint area
        self.display.tft.fill_rect(
            185,
            68,
            125,
            25,
            theme.BACKGROUND
        )

        # Current target character
        self.display.tft.text(
            self.display.font,
            self.target,
            24,
            68,
            theme.TARGET
        )

        # Optional Morse pattern hint
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
                theme.PATTERN
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
            theme.BACKGROUND
        )

        if self.input_pattern:

            self.display.tft.text(
                self.display.font,
                self.input_pattern,
                10,
                130,
                theme.INPUT
            )

        if self.input_character:

            self.display.tft.text(
                self.display.font,
                self.input_character,
                220,
                130,
                theme.INPUT
            )


    # -------------------------
    # Draw result
    # -------------------------

    def draw_result(self):

        self.display.tft.fill_rect(
            125,
            168,
            185,
            25,
            theme.BACKGROUND
        )

        if self.result_text:

            self.display.tft.text(
                self.display.font,
                self.result_text,
                125,
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
            "SEND",
            10,
            42,
            theme.LABEL
        )

        self.display.tft.text(
            self.display.font,
            "PATTERN",
            190,
            42,
            theme.LABEL
        )


        # -------------------------
        # User input headings
        # -------------------------

        self.display.tft.text(
            self.display.font,
            "YOU SENT",
            10,
            105,
            theme.LABEL
        )

        self.display.tft.text(
            self.display.font,
            "THAT IS",
            170,
            105,
            theme.LABEL
        )


        # -------------------------
        # Result heading
        # -------------------------

        self.display.tft.text(
            self.display.font,
            "RESULT",
            10,
            168,
            theme.LABEL
        )


        self.draw_target_area()

        self.draw_input()

        self.draw_result()

        self.draw_softkeys()
        self.display.divider(38)
        self.display.divider(112)
        self.display.divider(165)
        self.display.divider(205)

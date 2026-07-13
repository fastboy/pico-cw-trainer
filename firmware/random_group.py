from screen import Screen
from decoder import Decoder
from morse import MORSE

import config
import random
import st7789


class RandomGroup(Screen):

    GROUP_LENGTH = 3

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

        # Letters and digits available for groups
        self.characters = []

        for character in (
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            "1234567890"
        ):

            if character in MORSE:

                self.characters.append(
                    character
                )

        # Group currently shown to the user
        self.target_group = ""

        # Characters decoded from the user's
        # current or previous attempt
        self.sent_group = ""

        # Morse patterns sent by the user
        self.sent_patterns = []

        self.result_text = ""

        self.result_color = st7789.WHITE

        self.hint_visible = False

        self.incorrect_attempts = 0

        # True when the next paddle element
        # should begin a completely new attempt.
        self.starting_new_attempt = True


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

        self.select_group(
            clear_feedback=True
        )

        super().open()


    # -------------------------
    # Create random group
    # -------------------------

    def select_group(
        self,
        clear_feedback=True
    ):

        previous = self.target_group

        if not self.characters:

            self.target_group = "AAA"

        else:

            while True:

                group = ""

                for _ in range(
                    self.GROUP_LENGTH
                ):

                    group += random.choice(
                        self.characters
                    )

                if (
                    group != previous
                    or len(self.characters) == 1
                ):

                    self.target_group = group

                    break

        self.decoder.clear()

        self.incorrect_attempts = 0

        self.hint_visible = False

        self.starting_new_attempt = True

        if clear_feedback:

            self.sent_group = ""

            self.sent_patterns = []

            self.result_text = ""

            self.result_color = (
                st7789.WHITE
            )


    # -------------------------
    # Reset current attempt
    # -------------------------

    def begin_attempt(self):

        self.decoder.clear()

        self.sent_group = ""

        self.sent_patterns = []

        self.result_text = ""

        self.result_color = st7789.WHITE

        self.starting_new_attempt = False

        self.draw_sent()

        self.draw_result()


    # -------------------------
    # Front buttons
    # -------------------------
    #
    # SELECT = Back
    # DOWN   = Next group
    # UP     = Show / Hide hint
    # -------------------------

    def update(self, event):

        if event == "SELECT":

            return self.parent


        elif event == "DOWN":

            self.select_group(
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

        # Preserve the previous completed result
        # until the first element of the next
        # attempt is actually sent.
        if self.starting_new_attempt:

            self.begin_attempt()


        if element == dot_value:

            self.decoder.add_dot()


        elif element == dash_value:

            self.decoder.add_dash()


        self.draw_current_pattern()


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


        self.sent_patterns.append(
            pattern
        )

        if character:

            self.sent_group += character

        else:

            self.sent_group += "?"


        self.draw_sent()


        # The group is not complete yet.
        if len(self.sent_group) < len(
            self.target_group
        ):

            return


        # -------------------------
        # Correct group
        # -------------------------

        if self.sent_group == self.target_group:

            self.result_text = "CORRECT"

            self.result_color = (
                st7789.GREEN
            )

            print(
                "Target group:",
                self.target_group,
                "Sent:",
                self.sent_group,
                "CORRECT"
            )

            self.draw_sent()

            self.draw_result()

            # Select a new group while keeping
            # the previous correct answer visible.
            self.select_group(
                clear_feedback=False
            )

            self.draw_target_area()

            self.draw_softkeys()


        # -------------------------
        # Incorrect group
        # -------------------------

        else:

            self.incorrect_attempts += 1

            self.result_text = "INCORRECT"

            self.result_color = (
                st7789.RED
            )

            # After three incorrect complete
            # groups, reveal the correct Morse.
            if self.incorrect_attempts >= 3:

                self.hint_visible = True


            print(
                "Target group:",
                self.target_group,
                "Sent:",
                self.sent_group,
                "INCORRECT",
                self.incorrect_attempts
            )

            self.draw_sent()

            self.draw_result()

            self.draw_target_area()

            self.draw_softkeys()

            # Keep the completed incorrect attempt
            # visible until the next paddle element.
            self.decoder.clear()

            self.starting_new_attempt = True


    # -------------------------
    # Format target hint
    # -------------------------

    def get_hint_lines(self):

        lines = []

        current_line = ""

        for character in self.target_group:

            pattern = MORSE.get(
                character,
                ""
            )

            if current_line:

                candidate = (
                    current_line
                    + " "
                    + pattern
                )

            else:

                candidate = pattern


            # The normal font is approximately
            # 16 pixels wide. Keep each line short
            # enough to fit beside the target.
            if len(candidate) <= 12:

                current_line = candidate

            else:

                if current_line:

                    lines.append(
                        current_line
                    )

                current_line = pattern


        if current_line:

            lines.append(
                current_line
            )


        return lines[:2]


    # -------------------------
    # Draw target and hint
    # -------------------------

    def draw_target_area(self):

        self.display.tft.fill_rect(
            10,
            65,
            300,
            42,
            st7789.BLACK
        )

        # Group to send
        self.display.tft.text(
            self.display.font,
            self.target_group,
            24,
            68,
            st7789.GREEN
        )


        if self.hint_visible:

            hint_lines = (
                self.get_hint_lines()
            )

            y = 68

            for line in hint_lines:

                self.display.tft.text(
                    self.display.font,
                    line,
                    145,
                    y,
                    st7789.CYAN
                )

                y += 18


    # -------------------------
    # Draw unfinished pattern
    # -------------------------

    def draw_current_pattern(self):

        # The current decoder buffer can be
        # displayed after completed patterns.
        patterns = list(
            self.sent_patterns
        )

        if self.decoder.buffer:

            patterns.append(
                self.decoder.buffer
            )

        pattern_text = " ".join(
            patterns
        )

        self.display.tft.fill_rect(
            10,
            138,
            300,
            20,
            st7789.BLACK
        )

        if pattern_text:

            self.display.tft.text(
                self.display.font,
                pattern_text,
                10,
                138,
                st7789.WHITE
            )


    # -------------------------
    # Draw sent group
    # -------------------------

    def draw_sent(self):

        self.display.tft.fill_rect(
            10,
            122,
            300,
            38,
            st7789.BLACK
        )

        if self.sent_group:

            self.display.tft.text(
                self.display.font,
                self.sent_group,
                190,
                122,
                st7789.WHITE
            )


        pattern_text = " ".join(
            self.sent_patterns
        )

        if pattern_text:

            self.display.tft.text(
                self.display.font,
                pattern_text,
                10,
                140,
                st7789.WHITE
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
            st7789.BLACK
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
            "SEND GROUP",
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


        self.display.tft.text(
            self.display.font,
            "YOU SENT",
            10,
            105,
            st7789.YELLOW
        )

        self.display.tft.text(
            self.display.font,
            "THAT IS",
            170,
            105,
            st7789.YELLOW
        )


        self.display.tft.text(
            self.display.font,
            "RESULT",
            10,
            168,
            st7789.YELLOW
        )


        self.draw_target_area()

        self.draw_sent()

        self.draw_result()

        self.draw_softkeys()

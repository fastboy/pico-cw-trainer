import theme

from screen import Screen
from decoder import Decoder
from morse import MORSE

import config
import random


class CharacterGroups(Screen):

    MIN_GROUP_LENGTH = 3
    MAX_GROUP_LENGTH = 5

    # Number of consecutive correct groups
    # required before increasing the length.
    CORRECT_TO_ADVANCE = 5


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

        # Letters and digits available
        # for character groups.
        self.characters = []

        for character in (
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            "1234567890"
        ):

            if character in MORSE:

                self.characters.append(
                    character
                )

        # Group currently shown to the user.
        self.target_group = ""

        # Characters decoded from the user's
        # current or previous attempt.
        self.sent_group = ""

        # Completed Morse patterns sent
        # by the user.
        self.sent_patterns = []

        self.result_text = ""
        self.result_color = theme.TEXT

        self.hint_visible = False

        self.incorrect_attempts = 0

        # Current difficulty.
        self.group_length = (
            self.MIN_GROUP_LENGTH
        )

        # Consecutive correct groups at
        # the current difficulty.
        self.correct_streak = 0

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

        # Begin at three characters every
        # time the mode is opened.
        self.group_length = (
            self.MIN_GROUP_LENGTH
        )

        self.correct_streak = 0

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

            self.target_group = (
                "A" * self.group_length
            )

        else:

            while True:

                group = ""

                for _ in range(
                    self.group_length
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
            self.result_color = theme.TEXT


    # -------------------------
    # Reset current attempt
    # -------------------------

    def begin_attempt(self):

        self.decoder.clear()

        self.sent_group = ""
        self.sent_patterns = []

        self.result_text = ""
        self.result_color = theme.TEXT

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

        # Preserve the previous result until
        # the first element of the next
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

            self.correct_streak += 1

            self.result_text = "CORRECT"

            self.result_color = (
                theme.SUCCESS
            )

            print(
                "Target group:",
                self.target_group,
                "Sent:",
                self.sent_group,
                "CORRECT",
                "Streak:",
                self.correct_streak
            )

            self.draw_sent()
            self.draw_result()


            # Increase difficulty after the
            # required correct streak.
            if (
                self.correct_streak
                >= self.CORRECT_TO_ADVANCE
            ):

                self.correct_streak = 0

                if (
                    self.group_length
                    < self.MAX_GROUP_LENGTH
                ):

                    self.group_length += 1

                    print(
                        "Group length increased to:",
                        self.group_length
                    )


            # Select another target while
            # keeping the previous answer
            # and result visible.
            self.select_group(
                clear_feedback=False
            )

            self.draw_target_area()
            self.draw_softkeys()


        # -------------------------
        # Incorrect group
        # -------------------------

        else:

            # The progression requires
            # consecutive correct groups.
            self.correct_streak = 0

            self.incorrect_attempts += 1

            self.result_text = "INCORRECT"

            self.result_color = (
                theme.ERROR
            )

            # Reveal the expected Morse after
            # three complete incorrect attempts.
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

            # Keep the completed incorrect
            # attempt visible until the next
            # paddle element.
            self.decoder.clear()

            self.starting_new_attempt = True


    # -------------------------
    # Split Morse into lines
    # -------------------------

    def split_patterns(
        self,
        patterns,
        maximum_length
    ):

        lines = []
        current_line = ""

        for pattern in patterns:

            if current_line:

                candidate = (
                    current_line
                    + " "
                    + pattern
                )

            else:

                candidate = pattern


            if len(candidate) <= maximum_length:

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


        return lines


    # -------------------------
    # Expected Morse patterns
    # -------------------------

    def target_patterns(self):

        patterns = []

        for character in self.target_group:

            pattern = MORSE.get(
                character,
                ""
            )

            if pattern:

                patterns.append(
                    pattern
                )


        return patterns


    # -------------------------
    # Draw target and hint
    # -------------------------

    def draw_target_area(self):

        # Clear everything between
        # the first and second divider.
        self.display.tft.fill_rect(
            0,
            39,
            self.display.WIDTH,
            93,
            theme.BACKGROUND
        )

        # Section heading.
        self.display.tft.text(
            self.display.font,
            "SEND GROUP",
            10,
            42,
            theme.LABEL
        )

        # Group to send.
        self.display.tft.text(
            self.display.font,
            self.target_group,
            10,
            60,
            theme.TARGET
        )

        # Optional Morse hint.
        if self.hint_visible:

            lines = self.split_patterns(
                self.target_patterns(),
                18
            )

            y = 78

            for line in lines[:3]:

                self.display.tft.text(
                    self.display.font,
                    line,
                    10,
                    y,
                    theme.HINT
                )

                y += 18


    # -------------------------
    # Draw unfinished pattern
    # -------------------------

    def draw_current_pattern(self):

        patterns = list(
            self.sent_patterns
        )

        if self.decoder.buffer:

            patterns.append(
                self.decoder.buffer
            )


        self.draw_sent_content(
            patterns
        )


    # -------------------------
    # Draw decoded group and Morse
    # -------------------------

    def draw_sent_content(
        self,
        patterns
    ):

        # Clear everything below the
        # YOU SENT heading and above
        # the bottom divider.
        self.display.tft.fill_rect(
            0,
            153,
            self.display.WIDTH,
            67,
            theme.BACKGROUND
        )

        # -------------------------
        # Decoded group
        # -------------------------

        text_lines = [
            self.sent_group[:18],
            self.sent_group[18:36]
        ]

        y = 154

        for line in text_lines:

            if line:

                self.display.tft.text(
                    self.display.font,
                    line,
                    10,
                    y,
                    theme.INPUT
                )

            y += 18


        # -------------------------
        # Morse patterns
        # -------------------------

        pattern_lines = self.split_patterns(
            patterns,
            18
        )

        y = 188

        for line in pattern_lines[:2]:

            self.display.tft.text(
                self.display.font,
                line,
                10,
                y,
                theme.PATTERN
            )

            y += 17


    # -------------------------
    # Draw completed group
    # -------------------------

    def draw_sent(self):

        self.draw_sent_content(
            self.sent_patterns
        )


    # -------------------------
    # Draw result
    # -------------------------

    def draw_result(self):

        # Result appears beside YOU SENT.
        self.display.tft.fill_rect(
            165,
            135,
            145,
            18,
            theme.BACKGROUND
        )

        if self.result_text:

            self.display.tft.text(
                self.display.font,
                self.result_text,
                165,
                136,
                self.result_color
            )


    # -------------------------
    # Draw soft keys
    # -------------------------

    def draw_softkeys(self):

        if self.hint_visible:

            right_label = " HIDE"

        else:

            right_label = " HINT"


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

        # Target and optional hint.
        self.draw_target_area()

        # User-input heading.
        self.display.tft.text(
            self.display.font,
            "YOU SENT",
            10,
            136,
            theme.LABEL
        )

        # Dynamic content.
        self.draw_sent()
        self.draw_result()
        self.draw_softkeys()

        # Draw dividers last so clearing
        # rectangles cannot erase them.
        self.display.divider(
            38
        )

        self.display.divider(
            132
        )

        self.display.divider(
            220
        )

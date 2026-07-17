import theme

from screen import Screen
from decoder import Decoder
from morse import MORSE

import config
import random


# -------------------------
# Callsign generation data
# -------------------------

PREFIXES = (

    # Sweden
    "SA",
    "SB",
    "SC",
    "SD",
    "SE",
    "SF",
    "SG",
    "SH",
    "SI",
    "SJ",
    "SK",
    "SL",
    "SM",
    "7S",
    "8S",

    # Poland
    "HF",
    "SN",
    "SO",
    "SP",
    "SQ",
    "SR",
    "3Z",

    # Germany
    "DA",
    "DB",
    "DC",
    "DD",
    "DF",
    "DG",
    "DH",
    "DJ",
    "DK",
    "DL",
    "DM",
    "DN",
    "DO",
    "DP",
    "DQ",
    "DR",

    # Nordic countries
    "LA",
    "LB",
    "LC",
    "LD",
    "LE",
    "LF",
    "LG",
    "LI",
    "LJ",
    "OZ",
    "OH",

    # Europe
    "F",
    "G",
    "M",
    "I",
    "EA",
    "CT",
    "EI",
    "OE",
    "OK",
    "OM",
    "PA",
    "ON",
    "HB",
    "S5",
    "9A",
    "YU",
    "LZ",
    "YO",

    # North America
    "K",
    "N",
    "W",
    "AA",
    "AB",
    "AC",
    "AD",
    "AE",
    "AF",
    "AG",
    "AI",
    "AJ",
    "AK",
    "VA",
    "VE"
)


SUFFIX_CHARACTERS = (
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
)


class Callsigns(Screen):

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

        # Callsign currently shown
        # to the user.
        self.target_callsign = ""

        # Callsign decoded from the
        # user's current attempt.
        self.sent_callsign = ""

        # Completed Morse patterns from
        # the user's attempt.
        self.sent_patterns = []

        self.result_text = ""
        self.result_color = theme.TEXT

        self.hint_visible = False

        self.incorrect_attempts = 0

        # Keeps the completed result visible
        # until the first element of the next
        # attempt is actually sent.
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

        self.select_callsign(
            clear_feedback=True
        )

        super().open()


    # -------------------------
    # Generate callsign
    # -------------------------

    def generate_callsign(self):

        prefix = random.choice(
            PREFIXES
        )

        number = str(
            random.randint(
                0,
                9
            )
        )

        # Most generated callsigns will use
        # two or three suffix letters.
        suffix_length = random.choice(
            (
                2,
                3
            )
        )

        suffix = ""

        for _ in range(
            suffix_length
        ):

            suffix += random.choice(
                SUFFIX_CHARACTERS
            )

        return (
            prefix
            + number
            + suffix
        )


    # -------------------------
    # Select another callsign
    # -------------------------

    def select_callsign(
        self,
        clear_feedback=True
    ):

        previous = self.target_callsign

        while True:

            callsign = (
                self.generate_callsign()
            )

            # Avoid showing exactly the same
            # callsign twice in a row.
            if callsign != previous:

                self.target_callsign = callsign

                break

        self.decoder.clear()

        self.incorrect_attempts = 0
        self.hint_visible = False
        self.starting_new_attempt = True

        if clear_feedback:

            self.sent_callsign = ""
            self.sent_patterns = []

            self.result_text = ""
            self.result_color = theme.TEXT


    # -------------------------
    # Begin another attempt
    # -------------------------

    def begin_attempt(self):

        self.decoder.clear()

        self.sent_callsign = ""
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
    # DOWN   = Next callsign
    # UP     = Show / Hide hint
    # -------------------------

    def update(self, event):

        if event == "SELECT":

            return self.parent


        elif event == "DOWN":

            self.select_callsign(
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

        # Keep the previous completed attempt
        # visible until the user actually starts
        # sending the next callsign.
        if self.starting_new_attempt:

            self.begin_attempt()


        if element == dot_value:

            self.decoder.add_dot()


        elif element == dash_value:

            self.decoder.add_dash()


        self.draw_current_patterns()


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

            self.sent_callsign += character

        else:

            self.sent_callsign += "?"


        self.draw_sent()


        # The callsign is not complete yet.
        if len(self.sent_callsign) < len(
            self.target_callsign
        ):

            return


        # -------------------------
        # Correct callsign
        # -------------------------

        if (
            self.sent_callsign
            == self.target_callsign
        ):

            self.result_text = "CORRECT"

            self.result_color = (
                theme.SUCCESS
            )

            print(
                "Target callsign:",
                self.target_callsign,
                "Sent:",
                self.sent_callsign,
                "CORRECT"
            )

            self.draw_sent()
            self.draw_result()

            # Automatically select another
            # callsign while keeping the previous
            # completed answer visible.
            self.select_callsign(
                clear_feedback=False
            )

            self.draw_target_area()
            self.draw_softkeys()


        # -------------------------
        # Incorrect callsign
        # -------------------------

        else:

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
                "Target callsign:",
                self.target_callsign,
                "Sent:",
                self.sent_callsign,
                "INCORRECT",
                self.incorrect_attempts
            )

            self.draw_sent()
            self.draw_result()

            self.draw_target_area()
            self.draw_softkeys()

            # Keep the completed incorrect
            # attempt visible until the next
            # paddle element is sent.
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

        for character in self.target_callsign:

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

        self.display.tft.text(
            self.display.font,
            "SEND CALL",
            10,
            42,
            theme.LABEL
        )

        self.display.tft.text(
            self.display.font,
            self.target_callsign,
            10,
            60,
            theme.TARGET
        )

        # Optional expected Morse hint.
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
    # Draw unfinished patterns
    # -------------------------

    def draw_current_patterns(self):

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
    # Draw decoded callsign
    # and Morse patterns
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
        # Decoded callsign
        # -------------------------

        text_lines = [
            self.sent_callsign[:18],
            self.sent_callsign[18:36]
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
    # Draw completed callsign
    # -------------------------

    def draw_sent(self):

        self.draw_sent_content(
            self.sent_patterns
        )


    # -------------------------
    # Draw result
    # -------------------------

    def draw_result(self):

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

from screen import Screen
from decoder import Decoder
from morse import MORSE

import config
import random
import theme
import st7789


# -------------------------
# Word library
# -------------------------
#
# Short, common words are best for the first
# version because they fit on the display and
# are useful for learning character sequences.
# -------------------------

WORDS = (

    # Two letters
    "AM",
    "AN",
    "AS",
    "AT",
    "BE",
    "BY",
    "DO",
    "GO",
    "HE",
    "IF",
    "IN",
    "IS",
    "IT",
    "ME",
    "MY",
    "NO",
    "OF",
    "OH",
    "ON",
    "OR",
    "SO",
    "TO",
    "UP",
    "US",
    "WE",

    # Three letters
    "ALL",
    "AND",
    "ARE",
    "BAD",
    "BIG",
    "BOY",
    "CAN",
    "CAR",
    "CAT",
    "CUP",
    "DAY",
    "DOG",
    "END",
    "FAR",
    "FAST",
    "FIX",
    "FUN",
    "GET",
    "GOOD",
    "HAM",
    "HAS",
    "HAT",
    "HER",
    "HIM",
    "HIS",
    "HOT",
    "HOW",
    "KEY",
    "MAN",
    "MAP",
    "NEW",
    "NOT",
    "NOW",
    "OLD",
    "ONE",
    "OUR",
    "OUT",
    "RED",
    "RUN",
    "SAY",
    "SEA",
    "SEE",
    "SET",
    "SHE",
    "SUN",
    "TEN",
    "THE",
    "TOP",
    "TWO",
    "USE",
    "WAY",
    "WHO",
    "WHY",
    "YES",
    "YOU",

    # Four letters
    "BACK",
    "BALL",
    "BEST",
    "BLUE",
    "BOAT",
    "BOOK",
    "CALL",
    "CODE",
    "COLD",
    "COME",
    "DASH",
    "DOWN",
    "EASY",
    "FIND",
    "FIRE",
    "FIVE",
    "FROM",
    "GAME",
    "GOOD",
    "HAND",
    "HAVE",
    "HELP",
    "HOME",
    "KEEP",
    "KNOW",
    "LAST",
    "LEFT",
    "LIKE",
    "LINE",
    "LOOK",
    "MAKE",
    "NAME",
    "NEXT",
    "NINE",
    "OPEN",
    "PLAY",
    "READ",
    "RIGHT",
    "SEND",
    "SHOW",
    "SLOW",
    "SOME",
    "STOP",
    "TEST",
    "TIME",
    "TONE",
    "TURN",
    "WANT",
    "WATER",
    "WORD",
    "WORK",
    "ZERO",

    # Five letters
    "ABOUT",
    "AFTER",
    "AGAIN",
    "BLACK",
    "CALLS",
    "CHARM",
    "CLEAR",
    "CLOSE",
    "FIRST",
    "GREEN",
    "HELLO",
    "LEARN",
    "LIGHT",
    "MORSE",
    "OTHER",
    "POWER",
    "PRESS",
    "RADIO",
    "READY",
    "RIGHT",
    "SHORT",
    "SOUND",
    "START",
    "STILL",
    "THREE",
    "TRAIN",
    "UNDER",
    "WHITE",
    "WORLD"
)


class Words(Screen):

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

        # Only keep words containing characters
        # that exist in the Morse dictionary.
        self.words = []

        for word in WORDS:

            valid = True

            for character in word:

                if character not in MORSE:

                    valid = False

                    break

            if valid:

                self.words.append(
                    word
                )

        # Word currently shown to the user
        self.target_word = ""

        # Word decoded from the user's attempt
        self.sent_word = ""

        # Completed Morse patterns from the
        # user's attempt
        self.sent_patterns = []

        self.result_text = ""

        self.result_color = st7789.WHITE

        self.hint_visible = False

        self.incorrect_attempts = 0

        # Keeps a completed result visible until
        # the first element of the next attempt.
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

        self.select_word(
            clear_feedback=True
        )

        super().open()


    # -------------------------
    # Select random word
    # -------------------------

    def select_word(
        self,
        clear_feedback=True
    ):

        previous = self.target_word

        if not self.words:

            self.target_word = "MORSE"

        else:

            self.target_word = random.choice(
                self.words
            )

            # Avoid the same word twice in a row.
            if len(self.words) > 1:

                while self.target_word == previous:

                    self.target_word = random.choice(
                        self.words
                    )

        self.decoder.clear()

        self.incorrect_attempts = 0

        self.hint_visible = False

        self.starting_new_attempt = True

        if clear_feedback:

            self.sent_word = ""

            self.sent_patterns = []

            self.result_text = ""

            self.result_color = (
                st7789.WHITE
            )


    # -------------------------
    # Begin another attempt
    # -------------------------

    def begin_attempt(self):

        self.decoder.clear()

        self.sent_word = ""

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
    # DOWN   = Next word
    # UP     = Show / Hide hint
    # -------------------------

    def update(self, event):

        if event == "SELECT":

            return self.parent


        elif event == "DOWN":

            self.select_word(
                clear_feedback=True
            )

            self.draw()


        elif event == "UP":

            # Showing the answer is always allowed.
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

        # Keep the previous completed word visible
        # until the first element of the next
        # attempt is sent.
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

        # Ignore the later word-space event.
        if not pattern:

            return


        self.sent_patterns.append(
            pattern
        )

        if character:

            self.sent_word += character

        else:

            self.sent_word += "?"


        self.draw_sent()


        # The word is not complete yet.
        if len(self.sent_word) < len(
            self.target_word
        ):

            return


        # -------------------------
        # Correct word
        # -------------------------

        if self.sent_word == self.target_word:

            self.result_text = "CORRECT"

            self.result_color = (
                theme.SUCCESS
            )

            print(
                "Target word:",
                self.target_word,
                "Sent:",
                self.sent_word,
                "CORRECT"
            )

            self.draw_sent()

            self.draw_result()

            # Automatically select another word,
            # but leave the previous correct word
            # and Morse patterns visible.
            self.select_word(
                clear_feedback=False
            )

            self.draw_target_area()

            self.draw_softkeys()


        # -------------------------
        # Incorrect word
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
                "Target word:",
                self.target_word,
                "Sent:",
                self.sent_word,
                "INCORRECT",
                self.incorrect_attempts
            )

            self.draw_sent()

            self.draw_result()

            self.draw_target_area()

            self.draw_softkeys()

            # Keep the completed incorrect attempt
            # visible until the paddle is used again.
            self.decoder.clear()

            self.starting_new_attempt = True


    # -------------------------
    # Split text into lines
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

        for character in self.target_word:

            patterns.append(
                MORSE.get(
                    character,
                    ""
                )
            )

        return patterns


    # -------------------------
    # Draw target and hint
    # -------------------------

    def draw_target_area(self):

        # Clear everything between the
        # top and middle dividers.
        self.display.tft.fill_rect(
            0,
            39,
            self.display.WIDTH,
            93,
            theme.BACKGROUND
        )

        # Section heading
        self.display.tft.text(
            self.display.font,
            "SEND WORD",
            10,
            42,
            theme.LABEL
        )

        # Word to send
        self.display.tft.text(
            self.display.font,
            self.target_word,
            10,
            60,
            theme.TARGET
        )

        # Optional Morse hint
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
    # Draw current unfinished input
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
    # Draw decoded text and Morse
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
        # Decoded text
        # -------------------------
        #
        # Up to 18 characters per line.
        # Two lines are available.
        # -------------------------

        text_lines = [
            self.sent_word[:18],
            self.sent_word[18:36]
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
    # Draw sent word
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

        # Target and optional hint
        self.draw_target_area()

        # User input heading
        self.display.tft.text(
            self.display.font,
            "YOU SENT",
            10,
            136,
            theme.LABEL
        )

        # Dynamic content
        self.draw_sent()

        self.draw_result()

        self.draw_softkeys()

        # Draw dividers last so the clearing
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

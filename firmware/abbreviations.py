import theme

from screen import Screen
from decoder import Decoder
from morse import MORSE

import config
import random


# -------------------------------------------------
# Common CW abbreviations
# -------------------------------------------------
#
# Each entry contains:
#
#     meaning shown on screen
#     abbreviation expected from the student
#
# Unlike prosigns, these are transmitted as
# ordinary separate Morse characters.
#
# Example:
#
#     THANKS -> TNX
#
#     T     N      X
#     -     -.     -..-
#
# Q-codes are intentionally excluded because
# they belong in the separate Q-Codes trainer.
# -------------------------------------------------

ABBREVIATIONS = (

    # -------------------------
    # Basic conversation
    # -------------------------

    ("ABOUT",          "ABT"),
    ("AGAIN",          "AGN"),
    ("ALL",            "ALL"),
    ("ALSO",           "ALSO"),
    ("AND",            "ES"),
    ("ARE",            "R"),
    ("BECAUSE",        "BC"),
    ("BEFORE",         "B4"),
    ("CAN",            "CAN"),
    ("CONFIRM",        "CFM"),
    ("COPY",           "CPY"),
    ("DID",            "DID"),
    ("DO",             "DO"),
    ("FROM",           "DE"),
    ("HAVE",           "HV"),
    ("HERE",           "HR"),
    ("HOW",            "HW"),
    ("IS",             "IS"),
    ("LATER",          "LTR"),
    ("MESSAGE",        "MSG"),
    ("NOTHING",        "NIL"),
    ("NOW",            "NW"),
    ("NUMBER",         "NR"),
    ("PLEASE",         "PSE"),
    ("RECEIVED",       "R"),
    ("REPORT",         "RPT"),
    ("SAID",           "SED"),
    ("SORRY",          "SRI"),
    ("THAT",           "THT"),
    ("THANKS",         "TNX"),
    ("THANK YOU",      "TU"),
    ("THE",            "THE"),
    ("THIS",           "THIS"),
    ("VERY",           "VY"),
    ("WITH",           "WID"),
    ("WOULD",          "WUD"),
    ("YOU",            "U"),
    ("YOUR",           "UR"),


    # -------------------------
    # Greetings and farewells
    # -------------------------

    ("GOOD DAY",       "GD"),
    ("GOOD EVENING",   "GE"),
    ("GOOD MORNING",   "GM"),
    ("GOOD NIGHT",     "GN"),
    ("GOODBYE",        "GB"),
    ("SEE YOU",        "CU"),
    ("SEE YOU LATER",  "CUL"),
    ("SEE YOU AGAIN",  "CUAGN"),
    ("BEST REGARDS",   "73"),
    ("LOVE KISSES",    "88"),


    # -------------------------
    # Reactions and comments
    # -------------------------

    ("EXCELLENT",      "FB"),
    ("GOOD",           "GUD"),
    ("GOOD LUCK",      "GL"),
    ("LAUGHTER",       "HI"),
    ("OK",             "OK"),
    ("YES",            "YES"),
    ("NO",             "N"),


    # -------------------------
    # Operator and station
    # -------------------------

    ("AMATEUR",        "HAM"),
    ("CALLING",        "CLG"),
    ("CALLSIGN",       "CALL"),
    ("CONTACT",        "QSO"),
    ("DISTANT",        "DX"),
    ("OPERATOR",       "OP"),
    ("OLD MAN",        "OM"),
    ("STATION",        "STN"),
    ("WOMAN OP",       "YL"),
    ("WIFE",           "XYL"),


    # -------------------------
    # Radio equipment
    # -------------------------

    ("ANTENNA",        "ANT"),
    ("GROUND",         "GND"),
    ("POWER",          "PWR"),
    ("RECEIVER",       "RCVR"),
    ("RADIO",          "RIG"),
    ("SIGNAL",         "SIG"),
    ("TRANSMITTER",    "TX"),


    # -------------------------
    # Operating
    # -------------------------

    ("BREAK IN",       "BK"),
    ("CALL ANYONE",    "CQ"),
    ("CONDITIONS",     "CONDX"),
    ("CONTACTED",      "WKD"),
    ("SCHEDULE",       "SKED"),
    ("TESTING",        "TEST"),
    ("WORKING",        "WKG"),
    ("WEATHER",        "WX"),


    # -------------------------
    # Common short forms
    # -------------------------

    ("FINE BUSINESS",  "FB"),
    ("FOR",            "FER"),
    ("GO AHEAD",       "GA"),
    ("WILL",           "WL"),
    ("TEMPERATURE",    "TEMP"),
)
# -------------------------------------------------
# Reverse lookup
# -------------------------------------------------
#
# Used to show the meaning of an abbreviation
# transmitted by the student.
# -------------------------------------------------

ABBREVIATION_MEANING = {}

for meaning, abbreviation in ABBREVIATIONS:

    # Some abbreviations may have more than
    # one possible interpretation.
    #
    # Keep the first meaning from the table.
    if abbreviation not in ABBREVIATION_MEANING:

        ABBREVIATION_MEANING[
            abbreviation
        ] = meaning

class Abbreviations(Screen):

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

        # Keep only abbreviations whose
        # characters exist in MORSE.
        self.abbreviations = []


        for meaning, abbreviation in ABBREVIATIONS:

            valid = True

            for character in abbreviation:

                if character not in MORSE:

                    valid = False
                    break

            if valid:

                self.abbreviations.append(
                    (
                        meaning,
                        abbreviation
                    )
                )


        # Current exercise
        self.target_meaning = ""
        self.target_abbreviation = ""

        # User input
        self.input_abbreviation = ""
        self.input_patterns = []

        self.result_text = ""
        self.result_color = theme.TEXT

        self.hint_visible = False

        self.wrong_attempts = 0

        # Meaning represented by the abbreviation
        # transmitted by the student.
        self.input_meaning = ""


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

        self.select_abbreviation(
            clear_feedback=True
        )

        super().open()


    # -------------------------
    # Select random abbreviation
    # -------------------------

    def select_abbreviation(
        self,
        clear_feedback=True
    ):

        previous = self.target_abbreviation

        if not self.abbreviations:

            self.target_meaning = "THANKS"
            self.target_abbreviation = "TNX"

        else:

            (
                self.target_meaning,
                self.target_abbreviation
            ) = random.choice(
                self.abbreviations
            )

            # Avoid selecting the same answer
            # twice in a row when possible.
            if len(self.abbreviations) > 1:

                while (
                    self.target_abbreviation
                    == previous
                ):

                    (
                        self.target_meaning,
                        self.target_abbreviation
                    ) = random.choice(
                        self.abbreviations
                    )


        self.decoder.clear()

        self.wrong_attempts = 0

        # Hide hint for every new target.
        self.hint_visible = False


        if clear_feedback:

            self.input_abbreviation = ""
            self.input_patterns = []
            self.input_meaning = ""

            self.result_text = ""
            self.result_color = theme.TEXT


    # -------------------------
    # Front buttons
    # -------------------------
    #
    # SELECT = Back
    # DOWN   = Next abbreviation
    # UP     = Show / Hide hint
    # UP_REPEAT = Show HELP
    # -------------------------

    def update(self, event):

        if event == "SELECT":

            return self.parent


        elif event == "DOWN":

            self.select_abbreviation(
                clear_feedback=True
            )

            self.draw()


        elif event == "UP":

            self.hint_visible = (
                not self.hint_visible
            )

            self.draw_target_area()
            self.draw_softkeys()


        elif event == "UP_REPEAT":

            return "abbreviations_help"


        return None


    # -------------------------
    # Begin a new attempt
    # -------------------------

    def begin_attempt(self):

        self.decoder.clear()

        self.input_abbreviation = ""
        self.input_patterns = []

        self.result_text = ""
        self.result_color = theme.TEXT

        self.draw_input()
        self.draw_result()


    # -------------------------
    # Receive keyer elements
    # -------------------------

    def add_element(
        self,
        element,
        dot_value,
        dash_value
    ):

        # A completed answer remains visible until
        # the first paddle element of the next one.
        #
        # Decoder.buffer is empty between letters,
        # so also check whether a completed result
        # is currently displayed.
        if self.result_text:

            self.begin_attempt()


        if element == dot_value:

            self.decoder.add_dot()


        elif element == dash_value:

            self.decoder.add_dash()


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


        self.input_patterns.append(
            pattern
        )


        if character:

            self.input_abbreviation += (
                character
            )

        else:

            self.input_abbreviation += "?"

        # Show the meaning when the transmitted
        # abbreviation is recognised.
        self.input_meaning = (
            ABBREVIATION_MEANING.get(
                self.input_abbreviation,
                ""
            )
        )


        self.draw_input()


        # Not enough characters yet.
        if len(
            self.input_abbreviation
        ) < len(
            self.target_abbreviation
        ):

            return


        # -------------------------
        # Correct answer
        # -------------------------

        if (
            len(self.input_abbreviation)
            >= len(self.target_abbreviation)
            and not self.input_meaning
            ):

                self.input_meaning = "?"

        if (
            self.input_abbreviation
            == self.target_abbreviation
        ):

            self.result_text = "CORRECT"

            self.result_color = (
                theme.SUCCESS
            )

            print(
                "Meaning:",
                self.target_meaning,
                "Target:",
                self.target_abbreviation,
                "Input:",
                self.input_abbreviation,
                "CORRECT"
            )

            self.draw_input()
            self.draw_result()

            # Select the next exercise while
            # keeping the completed answer visible.
            self.select_abbreviation(
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

            # Reveal the answer after
            # three incorrect attempts.
            if self.wrong_attempts >= 3:

                self.hint_visible = True


            print(
                "Meaning:",
                self.target_meaning,
                "Target:",
                self.target_abbreviation,
                "Input:",
                self.input_abbreviation,
                "INCORRECT",
                self.wrong_attempts
            )

            self.draw_input()
            self.draw_result()

            self.draw_target_area()
            self.draw_softkeys()

            # Prepare for another attempt
            # at the same abbreviation.
            self.decoder.clear()


    # -------------------------
    # Expected Morse patterns
    # -------------------------

    def target_patterns(self):

        patterns = []

        for character in (
            self.target_abbreviation
        ):

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
    # Build input-pattern text
    # -------------------------

    def input_pattern_text(self):

        patterns = list(
            self.input_patterns
        )

        # Add the character currently
        # being transmitted.
        if self.decoder.buffer:

            patterns.append(
                self.decoder.buffer
            )

        return " ".join(
            patterns
        )


    # -------------------------
    # Draw current target
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

        # SEND and meaning on one line.
        self.display.tft.text(
            self.display.font,
            "SEND",
            10,
            42,
            theme.LABEL
        )

        self.display.tft.text(
            self.display.font,
            self.target_meaning,
            105,
            42,
            theme.TARGET
        )


        # Optional answer and Morse hint.
        if self.hint_visible:

            self.display.tft.text(
                self.display.font,
                self.target_abbreviation,
                10,
                68,
                theme.HINT
            )

            pattern_text = " ".join(
                self.target_patterns()
            )

            self.display.tft.text(
                self.display.font,
                pattern_text,
                10,
                94,
                theme.HINT
            )


    # -------------------------
    # Draw user input
    # -------------------------

    def draw_input(self):

        # Clear input-content area without
        # touching the heading or dividers.
        self.display.tft.fill_rect(
            0,
            153,
            self.display.WIDTH,
            67,
            theme.BACKGROUND
        )

        # Abbreviation transmitted by
        # the student.
        if self.input_abbreviation:

            self.display.tft.text(
                self.display.font,
                self.input_abbreviation,
                10,
                154,
                theme.INPUT
            )

        # Meaning of the transmitted
        # abbreviation.
        if self.input_meaning:

            self.display.tft.text(
                self.display.font,
                self.input_meaning,
                135,
                154,
                theme.INPUT
            )


        pattern_text = (
            self.input_pattern_text()
        )

        if pattern_text:

            self.display.tft.text(
                self.display.font,
                pattern_text,
                10,
                188,
                theme.PATTERN
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
    # Draw help screen
    # -------------------------

    def draw_help(self):

        self.display.clear()

        self.display.title()

        self.display.tft.text(
            self.display.font,
            "ABBREVIATIONS",
            10,
            42,
            theme.TITLE
        )

        help_lines = (
            "CW ABBREVIATIONS",
            "MAKE MESSAGES",
            "SHORTER AND FASTER.",
            "",
            "PLEASE BECOMES PSE",
            "THANKS BECOMES TNX",
            "YOUR BECOMES UR",
            "",
            "SEND EACH LETTER",
            "SEPARATELY."
        )

        y = 68

        for line in help_lines:

            if line:

                self.display.tft.text(
                    self.display.font,
                    line,
                    10,
                    y,
                    theme.TEXT
                )

            y += 16


        self.display.show_softkeys(
            "CLOSE",
            "CLOSE",
            "CLOSE"
        )

        self.display.divider(
            38
        )

        self.display.divider(
            220
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

        # Meaning and optional hint.
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
        self.draw_input()
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


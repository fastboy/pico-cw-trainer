import theme

from screen import Screen
from decoder import Decoder
from morse import MORSE

import config
import random


# -------------------------
# Q-code training material
# -------------------------
#
# Each entry contains:
#
#     Q-code
#     first meaning line
#     optional second meaning line
#
# The meaning lines are kept short enough
# to fit the 320-pixel display.
# -------------------------

Q_CODES = (

    (
        "QRL",
        "ARE YOU BUSY?",
        ""
    ),

    (
        "QRM",
        "INTERFERENCE",
        ""
    ),

    (
        "QRN",
        "STATIC NOISE",
        ""
    ),

    (
        "QRO",
        "INCREASE POWER",
        ""
    ),

    (
        "QRP",
        "REDUCE POWER",
        ""
    ),

    (
        "QRQ",
        "SEND FASTER",
        ""
    ),

    (
        "QRS",
        "SEND SLOWER",
        ""
    ),

    (
        "QRT",
        "STOP SENDING",
        ""
    ),

    (
        "QRU",
        "NOTHING FOR YOU",
        ""
    ),

    (
        "QRV",
        "ARE YOU READY?",
        ""
    ),

    (
        "QRX",
        "WAIT",
        ""
    ),

    (
        "QRZ",
        "WHO IS CALLING?",
        ""
    ),

    (
        "QSB",
        "SIGNAL FADING",
        ""
    ),

    (
        "QSL",
        "RECEIVED OK",
        ""
    ),

    (
        "QSO",
        "RADIO CONTACT",
        ""
    ),

    (
        "QSY",
        "CHANGE FREQUENCY",
        ""
    ),

    (
        "QTH",
        "MY LOCATION",
        ""
    ),

    (
        "QTR",
        "CORRECT TIME",
        ""
    ),

)


# -------------------------
# Meaning lookup
# -------------------------
#
# Used after a completed answer so the
# transmitted Q-code can be displayed
# together with its meaning.
# -------------------------

Q_CODE_MEANING = {}

for code, line_1, line_2 in Q_CODES:

    meaning = line_1

    if line_2:

        meaning += " " + line_2

    Q_CODE_MEANING[code] = meaning


class QCodes(Screen):

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


        # -------------------------
        # Current target
        # -------------------------

        self.target_code = ""
        self.target_line_1 = ""
        self.target_line_2 = ""


        # -------------------------
        # User input
        # -------------------------

        self.sent_code = ""
        self.sent_patterns = []


        # -------------------------
        # Result and hint
        # -------------------------

        self.result_text = ""
        self.result_color = theme.TEXT

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

        self.select_q_code(
            clear_feedback=True
        )

        super().open()


    # -------------------------
    # Select random Q-code
    # -------------------------

    def select_q_code(
        self,
        clear_feedback=True
    ):

        previous_code = (
            self.target_code
        )

        selected = random.choice(
            Q_CODES
        )

        # Avoid showing exactly the same
        # Q-code twice in a row.
        if len(Q_CODES) > 1:

            while selected[0] == previous_code:

                selected = random.choice(
                    Q_CODES
                )


        self.target_code = selected[0]
        self.target_line_1 = selected[1]
        self.target_line_2 = selected[2]

        self.decoder.clear()

        self.wrong_attempts = 0
        self.hint_visible = False


        if clear_feedback:

            self.sent_code = ""
            self.sent_patterns = []

            self.result_text = ""
            self.result_color = theme.TEXT


    # -------------------------
    # Front buttons
    # -------------------------
    #
    # SELECT    = Back
    # DOWN      = Next Q-code
    # UP        = Show / hide hint
    # UP_REPEAT = Open help
    # -------------------------

    def update(self, event):

        if event == "SELECT":

            return self.parent


        elif event == "DOWN":

            self.select_q_code(
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

            return "q_codes_help"


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

        # When the first Morse element of a new
        # attempt arrives, clear the previous
        # completed answer and result.
        #
        # The previous answer therefore remains
        # visible until the learner starts sending
        # the next one.
        if (
            not self.sent_code
            and not self.decoder.buffer
        ):

            self.sent_patterns = []

            self.result_text = ""
            self.result_color = theme.TEXT

            self.draw_input()
            self.draw_result()


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


        # Ignore word-space events generated
        # after a longer period of silence.
        if not pattern:

            return


        # Save the actual pattern sent for
        # this individual letter.
        self.sent_patterns.append(
            pattern
        )


        # Unknown Morse patterns are displayed
        # as a question mark.
        if character:

            self.sent_code += character

        else:

            self.sent_code += "?"


        self.draw_input()


        # Wait until three characters have
        # been decoded.
        if len(self.sent_code) < 3:

            return


        # -------------------------
        # Correct answer
        # -------------------------

        if self.sent_code == self.target_code:

            self.result_text = "CORRECT"

            self.result_color = (
                theme.SUCCESS
            )


            print(
                "Target:",
                self.target_code,
                "Input:",
                self.sent_code,
                "CORRECT"
            )


            # Show the completed answer before
            # selecting the next target.
            self.draw_input()
            self.draw_result()


            # Select another Q-code but preserve
            # the completed answer and result.
            self.select_q_code(
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


            # Reveal the correct answer after
            # three unsuccessful attempts.
            if self.wrong_attempts >= 3:

                self.hint_visible = True


            print(
                "Target:",
                self.target_code,
                "Input:",
                self.sent_code,
                "INCORRECT",
                self.wrong_attempts
            )


            self.draw_input()
            self.draw_result()

            self.draw_target_area()
            self.draw_softkeys()


            # Prepare for another attempt at
            # the same Q-code.
            self.sent_code = ""
            self.sent_patterns = []

            self.decoder.clear()


    # -------------------------
    # Build Morse hint
    # -------------------------

    def get_target_pattern(self):

        patterns = []

        for character in self.target_code:

            pattern = MORSE.get(
                character,
                ""
            )

            if pattern:

                patterns.append(
                    pattern
                )


        return " ".join(
            patterns
        )


    # -------------------------
    # Draw current target
    # -------------------------

    def draw_target_area(self):

        # Clear everything between the
        # first and second dividers.
        self.display.tft.fill_rect(
            0,
            39,
            self.display.WIDTH,
            93,
            theme.BACKGROUND
        )


        # -------------------------
        # Instruction
        # -------------------------

        self.display.tft.text(
            self.display.font,
            "SEND",
            10,
            42,
            theme.LABEL
        )


        # -------------------------
        # Meaning to translate
        # -------------------------

        self.display.tft.text(
            self.display.font,
            self.target_line_1,
            90,
            42,
            theme.TARGET
        )


        if self.target_line_2:

            self.display.tft.text(
                self.display.font,
                self.target_line_2,
                90,
                65,
                theme.TARGET
            )


        # -------------------------
        # Optional hint
        # -------------------------

        if self.hint_visible:

            hint = (
                self.target_code
                + "  "
                + self.get_target_pattern()
            )

            self.display.tft.text(
                self.display.font,
                hint,
                10,
                96,
                theme.HINT
            )


    # -------------------------
    # Draw user input
    # -------------------------

    def draw_input(self):

        # Clear the input-content area without
        # touching YOU SENT or the divider.
        self.display.tft.fill_rect(
            0,
            153,
            self.display.WIDTH,
            67,
            theme.BACKGROUND
        )


        # -------------------------
        # Decoded Q-code
        # -------------------------

        if self.sent_code:

            self.display.tft.text(
                self.display.font,
                self.sent_code,
                10,
                154,
                theme.INPUT
            )


            # Display the meaning beside a valid
            # completed Q-code.
            meaning = Q_CODE_MEANING.get(
                self.sent_code,
                ""
            )

            if meaning:

                # The remaining space beside the
                # three-letter code fits around
                # thirteen characters.
                meaning = meaning[:13]

                self.display.tft.text(
                    self.display.font,
                    meaning,
                    90,
                    154,
                    theme.TEXT
                )


        # -------------------------
        # Morse patterns sent
        # -------------------------

        patterns = list(
            self.sent_patterns
        )


        # Include the live pattern while the
        # current character is still being sent.
        if self.decoder.buffer:

            patterns.append(
                self.decoder.buffer
            )


        pattern_text = " ".join(
            patterns
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
    # Draw softkeys
    # -------------------------

    def draw_softkeys(self):

        if self.hint_visible:

            right_bottom = "HIDE"

        else:

            right_bottom = "HINT"


        self.display.show_softkeys(
            ("", "BACK"),
            ("", "NEXT"),
            ("HELP", right_bottom)
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


        # Target meaning and optional hint.
        self.draw_target_area()


        # Input heading.
        self.display.tft.text(
            self.display.font,
            "YOU SENT",
            10,
            136,
            theme.LABEL
        )


        # Dynamic screen content.
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

import theme

from screen import Screen
from decoder import Decoder

import config
import random


# -------------------------------------------------
# Prosigns
# -------------------------------------------------
#
# Each entry contains:
#
#     meaning shown to the user
#     prosign name
#     continuous Morse pattern
#
# The pattern has no letter spacing because
# a prosign is transmitted as one character.
# -------------------------------------------------

PROSIGNS = (

    (
        "END MESSAGE",
        "AR",
        ".-.-."
    ),

    (
        "WAIT",
        "AS",
        ".-..."
    ),

    (
        "BREAK",
        "BT",
        "-...-"
    ),

    (
        "END CONTACT",
        "SK",
        "...-.-"
    ),

    (
        "ONLY YOU GO",
        "KN",
        "-.--."
    ),

    (
        "START MESSAGE",
        "KA",
        "-.-.-"
    ),

    (
        "ERROR",
        "HH",
        "........"
    ),

    (
        "DISTRESS",
        "SOS",
        "...---..."
    ),

    (
        "CLOSING DOWN",
        "CL",
        "-.-..-.."
    ),

    (
        "NEW LINE",
        "AA",
        ".-.-"
    ),

)


# -------------------------------------------------
# Reverse lookup
# -------------------------------------------------
#
# This lets us find the prosign name from the
# continuous pattern sent by the user.
#
# Example:
#
#     "-...-" becomes "BT"
# -------------------------------------------------

PROSIGN_BY_PATTERN = {}

for meaning, prosign, pattern in PROSIGNS:

    PROSIGN_BY_PATTERN[
        pattern
    ] = prosign


class Prosigns(Screen):

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

        # Current table entry
        self.target_meaning = ""
        self.target_prosign = ""
        self.target_pattern = ""

        # Last continuous pattern
        # sent by the user.
        self.input_pattern = ""

        # Prosign represented by the pattern.
        self.input_prosign = ""

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

        self.select_prosign(
            clear_feedback=True
        )

        super().open()


    # -------------------------
    # Select random prosign
    # -------------------------

    def select_prosign(
        self,
        clear_feedback=True
    ):

        previous = self.target_prosign

        if not PROSIGNS:

            self.target_meaning = (
                "END MESSAGE"
            )

            self.target_prosign = "AR"

            self.target_pattern = (
                ".-.-."
            )

        else:

            entry = random.choice(
                PROSIGNS
            )

            (
                self.target_meaning,
                self.target_prosign,
                self.target_pattern
            ) = entry

            # Avoid showing the same prosign
            # twice in a row when possible.
            if len(PROSIGNS) > 1:

                while (
                    self.target_prosign
                    == previous
                ):

                    entry = random.choice(
                        PROSIGNS
                    )

                    (
                        self.target_meaning,
                        self.target_prosign,
                        self.target_pattern
                    ) = entry


        self.decoder.clear()

        self.wrong_attempts = 0

        # Hide the hint for every new target.
        self.hint_visible = False


        if clear_feedback:

            self.input_pattern = ""
            self.input_prosign = ""

            self.result_text = ""
            self.result_color = theme.TEXT


    # -------------------------
    # Front buttons
    # -------------------------
    #
    # SELECT = Back
    # DOWN   = Next prosign
    # UP     = Show / Hide hint
    # -------------------------

    def update(self, event):

        if event == "SELECT":

            return self.parent


        elif event == "DOWN":

            # Manually skip to another prosign.
            self.select_prosign(
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

            return "prosigns_help"


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
        # This lets the previous completed
        # answer remain visible while the next
        # target is already displayed.
        if not self.decoder.buffer:

            self.input_pattern = ""
            self.input_prosign = ""

            self.result_text = ""
            self.result_color = theme.TEXT

            self.draw_input()
            self.draw_result()


        if element == dot_value:

            self.decoder.add_dot()


        elif element == dash_value:

            self.decoder.add_dash()


        # Keep displaying the complete
        # continuous buffer while sending.
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


        self.input_pattern = pattern

        # Ignore the normal Morse character
        # returned by Decoder.
        #
        # Prosigns use their own continuous
        # pattern lookup table.
        self.input_prosign = (
            PROSIGN_BY_PATTERN.get(
                pattern,
                "?"
            )
        )


        # -------------------------
        # Correct answer
        # -------------------------

        if pattern == self.target_pattern:

            self.result_text = "CORRECT"

            self.result_color = (
                theme.SUCCESS
            )

            print(
                "Meaning:",
                self.target_meaning,
                "Target:",
                self.target_prosign,
                self.target_pattern,
                "Input:",
                pattern,
                self.input_prosign,
                "CORRECT"
            )

            # Display the completed answer.
            self.draw_input()
            self.draw_result()

            # Automatically select the next target,
            # but keep the previous sent pattern,
            # decoded prosign and result visible.
            self.select_prosign(
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
                "Meaning:",
                self.target_meaning,
                "Target:",
                self.target_prosign,
                self.target_pattern,
                "Input:",
                pattern,
                self.input_prosign,
                "INCORRECT",
                self.wrong_attempts
            )

            self.draw_input()
            self.draw_result()

            self.draw_target_area()
            self.draw_softkeys()

            # Prepare for another attempt
            # at the same prosign.
            self.decoder.clear()


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

        # SEND and meaning appear
        # together on one line.
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

        # Optional expected prosign hint.
        if self.hint_visible:

            self.display.tft.text(
                self.display.font,
                self.target_prosign,
                10,
                68,
                theme.HINT
            )

            self.display.tft.text(
                self.display.font,
                self.target_pattern,
                70,
                68,
                theme.HINT
            )


    # -------------------------
    # Draw user input
    # -------------------------

    def draw_input(self):

        # Clear the complete input-content area
        # without touching the heading or divider.
        self.display.tft.fill_rect(
            0,
            153,
            self.display.WIDTH,
            67,
            theme.BACKGROUND
        )

        # Prosign represented by the
        # continuous pattern.
        if self.input_prosign:

            self.display.tft.text(
                self.display.font,
                self.input_prosign,
                10,
                154,
                theme.INPUT
            )

        # Actual continuous dots and
        # dashes sent.
        if self.input_pattern:

            self.display.tft.text(
                self.display.font,
                self.input_pattern,
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
    # Draw soft keys
    # -------------------------

    def draw_softkeys(self):

        if self.hint_visible:

            right_label = " HIDE"

        else:

            right_label = " HINT"


        self.display.show_softkeys(
            ("", "BACK"),
            ("", "NEXT"),
            ("HELP", "HINT")
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

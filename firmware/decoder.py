import time

from morse import MORSE


# -------------------------
# Reverse Morse lookup
# -------------------------

DECODE = {}

for character, pattern in MORSE.items():

    DECODE[pattern] = character


class Decoder:

    def __init__(self, wpm=12):

        self.buffer = ""

        self.text = ""

        self.last_element = None

        # Duration of the most recently
        # received element, in dot-times:
        #
        # dot  = 1
        # dash = 3
        self.last_element_units = 1

        self.character_finished = False

        self.space_added = False

        self.set_speed(
            wpm
        )


    # -------------------------
    # Decoder speed
    # -------------------------

    def set_speed(self, wpm):

        self.wpm = wpm

        self.dot_time = int(
            1200 / wpm
        )


    # -------------------------
    # Add Morse elements
    # -------------------------

    def add_dot(self):

        self.buffer += "."

        self.last_element = time.ticks_ms()

        self.last_element_units = 1

        self.character_finished = False

        self.space_added = False


    def add_dash(self):

        self.buffer += "-"

        self.last_element = time.ticks_ms()

        self.last_element_units = 3

        self.character_finished = False

        self.space_added = False


    # -------------------------
    # Check character/word gaps
    # -------------------------

    def update(self):

        if self.last_element is None:

            return None


        silence_from_start = time.ticks_diff(

            time.ticks_ms(),

            self.last_element
        )


        # Events arrive when an element begins.
        # Include the duration of the last
        # element before measuring its gap.

        character_timeout = (

            self.last_element_units + 3

        ) * self.dot_time


        word_timeout = (

            self.last_element_units + 7

        ) * self.dot_time


        # -------------------------
        # End of character
        # -------------------------

        if (
            self.buffer
            and not self.character_finished
            and silence_from_start >= character_timeout
        ):

            return self.decode()


        # -------------------------
        # End of word
        # -------------------------

        if (
            self.character_finished
            and not self.space_added
            and silence_from_start >= word_timeout
        ):

            if (
                self.text
                and not self.text.endswith(" ")
            ):

                self.text += " "


            self.space_added = True

            return "", " "


        return None


    # -------------------------
    # Decode buffer
    # -------------------------

    def decode(self):

        pattern = self.buffer

        character = DECODE.get(
            pattern,
            "?"
        )

        self.text += character

        self.buffer = ""

        self.character_finished = True

        self.space_added = False

        return pattern, character


    # -------------------------
    # Clear session
    # -------------------------

    def clear(self):

        self.buffer = ""

        self.text = ""

        self.last_element = None

        self.last_element_units = 1

        self.character_finished = False

        self.space_added = False

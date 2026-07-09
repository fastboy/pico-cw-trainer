import time

from morse import MORSE


# Build reverse lookup table automatically
DECODE = {}

for letter, pattern in MORSE.items():
    DECODE[pattern] = letter


class Decoder:

    def __init__(self, timeout=1000):

        self.buffer = ""
        self.last_element = time.ticks_ms()
        self.timeout = timeout


    def add_dot(self):

        self.buffer += "."
        self.last_element = time.ticks_ms()


    def add_dash(self):

        self.buffer += "-"
        self.last_element = time.ticks_ms()


    def update(self):

        if self.buffer:

            if time.ticks_diff(
                time.ticks_ms(),
                self.last_element
            ) > self.timeout:

                return self.decode()

        return None


    def decode(self):

        letter = DECODE.get(
            self.buffer,
            "?"
        )

        pattern = self.buffer

        self.buffer = ""

        return pattern, letter
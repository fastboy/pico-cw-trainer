import time

from morse import MORSE


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

        # convert pattern to character

        letter = MORSE.get(
            self.buffer,
            "?"
        )

        pattern = self.buffer

        self.buffer = ""

        return pattern, letter
from morse import MORSE


class MorseEncoder:

    def __init__(self):
        pass

    def encode_char(self, ch):

        ch = ch.upper()

        if ch in MORSE:
            return MORSE[ch]

        return None

    def encode_text(self, text):

        patterns = []

        for ch in text.upper():

            if ch == " ":
                patterns.append("/")
                continue

            pattern = self.encode_char(ch)

            if pattern is not None:
                patterns.append(pattern)

        return patterns
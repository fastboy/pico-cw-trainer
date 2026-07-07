import time

class Keyer:

    def __init__(self, wpm=20):

        self.set_speed(wpm)

    def set_speed(self, wpm):

        self.wpm = wpm

        self.dot = 1.2 / wpm
        self.dash = self.dot * 3

        self.element_gap = self.dot
        self.letter_gap = self.dot * 3
        self.word_gap = self.dot * 7

    def get_timings(self):

        return {
            "dot": self.dot,
            "dash": self.dash,
            "element": self.element_gap,
            "letter": self.letter_gap,
            "word": self.word_gap
        }
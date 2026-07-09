import time


class Trainer:

    def __init__(self):
        self.start_time = None


    def press(self, element):

        self.element = element
        self.start_time = time.ticks_ms()


    def release(self):

        duration = time.ticks_diff(
            time.ticks_ms(),
            self.start_time
        )

        print(
            self.element,
            "held:",
            duration,
            "ms"
        )

        self.start_time = None
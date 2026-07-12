from screen import Screen
from decoder import Decoder


class SingleCharacter(Screen):

    def __init__(self, display):

        super().__init__()

        self.display = display

        self.parent = None

        self.decoder = Decoder()


    # -------------------------
    # Open screen
    # -------------------------

    def open(self):

        # Start every practice session clean
        self.decoder = Decoder()

        super().open()


    # -------------------------
    # Front buttons
    # -------------------------

    def update(self, event):

        if event == "SELECT":

            return self.parent

        return None


    # -------------------------
    # Receive keyer elements
    # -------------------------

    def add_element(self, element, dot_value, dash_value):

        if element == dot_value:

            self.decoder.add_dot()

        elif element == dash_value:

            self.decoder.add_dash()

        self.display.show_pattern(
            self.decoder.buffer
        )


    # -------------------------
    # Decoder timer
    # -------------------------

    def tick(self):

        result = self.decoder.update()

        if not result:

            return

        pattern, character = result

        self.display.show_letter(
            character
        )

        self.display.show_text(
            self.decoder.text
        )

        print(
            pattern,
            "=",
            character
        )


    # -------------------------
    # Draw
    # -------------------------

    def draw(self):

        self.display.title()

        self.display.show_speed(
            12
        )

        self.display.show_pattern(
            ""
        )

        self.display.show_letter(
            ""
        )

        self.display.show_text(
            ""
        )

        self.display.show_softkeys(

            "BACK",

            "",

            ""
        )
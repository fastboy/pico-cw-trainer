import config

from screen import Screen
from decoder import Decoder


class Practice(Screen):

    def __init__(self, display, keyer):

        super().__init__()

        self.display = display
        self.keyer = keyer

        self.decoder = Decoder(
            wpm=config.WPM
        )

        self.set_softkeys(

            "BACK",

            "",

            "CLEAR"
        )


    # -------------------------
    # Open screen
    # -------------------------

    def open(self):

        # Use the latest configured speed
        self.decoder.set_speed(
            config.WPM
        )
        self.keyer.set_speed(
            config.WPM
        )

        # Begin a fresh practice session
        self.decoder.clear()

        super().open()


    # -------------------------
    # Front buttons
    # -------------------------

    def update(self, event):

        # GP9 / left softkey
        if event == "SELECT":

            return self.parent


        # GP7 / right softkey
        elif event == "UP":

            self.clear()

        return None


    # -------------------------
    # Clear practice session
    # -------------------------

    def clear(self):

        self.decoder.clear()

        self.display.show_pattern(
            ""
        )

        self.display.show_letter(
            ""
        )

        self.display.show_text(
            ""
        )

        print("Practice cleared")


    # -------------------------
    # Receive keyer elements
    # -------------------------

    def add_element(
        self,
        element,
        dot_value,
        dash_value
    ):

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


        # A space event updates only the
        # running text, not the large letter.
        if character != " ":

            self.display.show_letter(
                character
            )

            print(
                pattern,
                "=",
                character
            )


        self.display.show_text(
            self.decoder.text
        )


    # -------------------------
    # Draw screen
    # -------------------------

    def draw(self):

        self.display.title()

        self.display.show_speed(
            config.WPM
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

        self.draw_softkeys()

import time
import config
from screen import Screen


class Tone(Screen):

    def __init__(self, display):

        self.display = display
        super().__init__()
        self.value = config.SIDETONE_FREQ

        self.MIN = 300
        self.MAX = 1200

    # -------------------------
    # Open editor
    # -------------------------

    def open(self):

        self.value = config.SIDETONE_FREQ
        super().open()

    # -------------------------
    # Button events
    # -------------------------

    def update(self, event):

        if event == "UP":

            self.up(10)


        elif event == "DOWN":

            self.down(10)


        elif event == "UP_REPEAT":

            self.up(50)


        elif event == "DOWN_REPEAT":

            self.down(50)
            
        elif event == "SELECT":

            return self.confirm()


        return None

    # -------------------------
    # Value adjustment
    # -------------------------

    def up(self, step=1):

        self.change(step)



    def down(self, step=1):

        self.change(-step)



    def change(self, amount):

        self.value += amount


        if self.value < self.MIN:

            self.value = self.MIN


        if self.value > self.MAX:

            self.value = self.MAX


        self.draw()

    # -------------------------
    # Confirm and return
    # -------------------------

    def confirm(self):

        config.SIDETONE_FREQ = self.value

        print("New Tone:", config.SIDETONE_FREQ)

        # Return the Settings screen object.
        # app.py can change directly to this screen.
        return self.parent

    # -------------------------
    # Draw editor
    # -------------------------

    def draw(self):

        self.display.tft.fill(0)


        self.display.tft.text(
            self.display.font,
            "TONE",
            110,
            20,
            0xFFE0
        )


        text = str(self.value) + " Hz"


        self.display.tft.text(
            self.display.font,
            text,
            100,
            100,
            0xFFFF
        )


        self.display.show_softkeys(
            "ACCEPT",
            "  -",
            "  +"
        )

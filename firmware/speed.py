import config
from screen import Screen


class Speed(Screen):

    def __init__(self, display):

        super().__init__()

        self.display = display

        self.value = config.WPM

        self.MIN = 5
        self.MAX = 60


    # -------------------------
    # Open editor
    # -------------------------

    def open(self):

        # Reload the current saved value whenever
        # the Speed editor is opened.
        self.value = config.WPM

        super().open()


    # -------------------------
    # Button events
    # -------------------------

    def update(self, event):

        if event == "UP":

            self.up(1)


        elif event == "DOWN":

            self.down(1)


        elif event == "UP_REPEAT":

            self.up(5)


        elif event == "DOWN_REPEAT":

            self.down(5)


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

        config.WPM = self.value

        print(
            "New WPM:",
            config.WPM
        )

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
            "SPEED",
            105,
            20,
            0xFFE0
        )


        text = (
            str(self.value)
            + " WPM"
        )


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


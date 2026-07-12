import config
from speed import Speed
from tone import Tone


class Settings:

    def __init__(self, display):

        self.display = display
        
        self.speed = Speed(display)
        self.tone = Tone(display)

        self.items = [
            "Speed",
            "Tone",
            "Back"
        ]

        self.index = 0


    def open(self):

        self.index = 0
        super().open()


    def up(self):

        self.index -= 1

        if self.index < 0:
            self.index = len(self.items) - 1

        self.draw()


    def down(self):

        self.index += 1

        if self.index >= len(self.items):
            self.index = 0

        self.draw()


    def select(self):

        item = self.items[self.index]

        print("Selected:", item)


        if item == "Speed":

                self.speed.open()

                return "speed"


        elif item == "Tone":

            self.tone.open()

            return "tone"


        elif item == "Back":

            return "back"



    def draw(self):

        self.display.tft.fill(0)


        self.display.tft.text(
            self.display.font,
            "SETTINGS",
            90,
            20,
            0xFFE0
        )


        y = 70

        for i, item in enumerate(self.items):

            if i == self.index:

                prefix = "> "

            else:

                prefix = "  "


            # left side
            self.display.tft.text(
                self.display.font,
                prefix + item,
                35,
                y,
                0xFFFF
            )


            # current values
            value = ""


            if item == "Speed":

                value = str(config.WPM) + " WPM"


            elif item == "Tone":

                value = str(config.SIDETONE_FREQ) + " Hz"


            self.display.tft.text(
                self.display.font,
                value,
                170,
                y,
                0xFFFF
            )


            y += 30



        self.display.show_softkeys(
            "CHANGE",
            "DOWN",
            " UP"
        )

import theme

from screen import Screen


class HelpScreen(Screen):

    def __init__(
        self,
        display,
        title,
        lines
    ):

        super().__init__()

        self.display = display

        self.help_title = title
        self.lines = lines

        self.parent = None


    # -------------------------
    # Front buttons
    # -------------------------
    #
    # Any button returns to the
    # screen that opened HELP.
    # -------------------------

    def update(self, event):

        if event in (
            "SELECT",
            "DOWN",
            "UP"
        ):

            return self.parent


        return None


    # -------------------------
    # Draw complete help screen
    # -------------------------

    def draw(self):

        self.display.clear()

        # Use the normal title position,
        # but replace CW TRAINER with the
        # name of the current help topic.
        self.display.tft.text(
            self.display.font,
            self.help_title,
            10,
            10,
            theme.TITLE
        )

        # Help text begins below
        # the top divider.
        y = 46

        for line in self.lines:

            if line:

                self.display.tft.text(
                    self.display.font,
                    line,
                    10,
                    y,
                    theme.TEXT
                )

            y += 16

            # Do not allow text to enter
            # the soft-key area.
            if y >= 218:

                break


        self.display.show_softkeys(
            "BACK",
            " BACK",
            " BACK"
        )

        self.display.divider(
            38
        )

        self.display.divider(
            220
        )

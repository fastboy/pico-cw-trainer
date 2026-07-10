class Menu:


    def __init__(self, display):

        self.display = display

        self.main_items = [
            "Practice",
            "Settings",
            "Keyer Mode",
            "About"
        ]

        self.settings_items = [
            "Speed",
            "Tone",
            "Back"
        ]

        self.items = self.main_items

        self.index = 0

        self.screen = "main"


    def open(self):

        self.screen = "main"
        self.items = self.main_items
        self.index = 0

        self.draw()


    def up(self):

        self.index -= 1

        if self.index < 0:
            self.index = len(self.items)-1

        self.draw()


    def down(self):

        self.index += 1

        if self.index >= len(self.items):
            self.index = 0

        self.draw()


    def select(self):

        selected = self.items[self.index]

        print("SELECT:", selected)


        if self.screen == "main":

            if selected == "Settings":

                self.screen = "settings"
                self.items = self.settings_items
                self.index = 0


        elif self.screen == "settings":

            if selected == "Back":

                self.screen = "main"
                self.items = self.main_items
                self.index = 0


        self.draw()



    def back(self):

        if self.screen == "settings":

            self.screen = "main"
            self.items = self.main_items
            self.index = 0

            self.draw()



    def draw(self):

        if self.screen == "main":

            title = "MENU"

        else:

            title = "SETTINGS"


        self.display.show_menu(
            title,
            self.items,
            self.index
        )
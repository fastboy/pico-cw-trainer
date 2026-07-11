from screen import Screen

class Menu(Screen):

    def __init__(self, display, settings=None):
        super().__init__()
        
        self.display = display
        self.settings = settings
        
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

        self.keyer_items = [
            "Straight",
            "Bug",
            "Iambic A",
            "Iambic B",
            "Back"
        ]

        self.items = self.main_items
        self.index = 0

        self.screen = "main"
        self.title = "MAIN MENU"

    def update(self, event):

        if event == "UP":

            self.up()


        elif event == "DOWN":

            self.down()


        elif event == "SELECT":

            return self.select()


        return None
    
    def open(self):

        self.screen = "main"
        self.title = "MAIN MENU"
        self.items = self.main_items
        self.index = 0

        self.draw()


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

        selected = self.items[self.index]

        print("SELECT:", selected)

        # -------------------------
        # MAIN MENU
        # -------------------------
        if self.screen == "main":

            if selected == "Practice":

                print("Practice selected")


            elif selected == "Settings":

                self.settings.open()

                return "settings"


            elif selected == "Keyer Mode":

                self.screen = "keyer"
                self.title = "KEYER MODE"
                self.items = self.keyer_items
                self.index = 0


            elif selected == "About":

                print("CW Trainer")
                print("Version 1.0")


        # -------------------------
        # SETTINGS
        # -------------------------
        elif self.screen == "settings":

            print("Setting:", selected)


        # -------------------------
        # KEYER MODE
        # -------------------------
        elif self.screen == "keyer":

            if selected == "Back":

                self.open()
                return

            print("Mode:", selected)


        self.draw()

    def update(self, event):

        if event == "UP":
            self.up()

        elif event == "DOWN":
            self.down()

        elif event == "SELECT":
            self.select()

        elif event == "UP_REPEAT":
            self.up()

        elif event == "DOWN_REPEAT":
            self.down()

    def draw(self):

        self.display.show_menu(
            self.title,
            self.items,
            self.index
        )


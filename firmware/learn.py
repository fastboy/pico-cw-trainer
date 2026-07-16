from screen import Screen


class Learn(Screen):

    # -------------------------
    # Menu layout
    # -------------------------

    ITEMS_PER_PAGE = 5


    def __init__(self, display):

        super().__init__()

        self.display = display

        self.title = "LEARN"

        self.items = [

            "Single Character",
            "Character Groups",
            "Random Words",
            "Callsigns",
            "Prosigns",

            "Q-Codes",
            "Mixed Text",
            "Game",
            "Back"
        ]

        self.index = 0


    # -------------------------
    # Open screen
    # -------------------------

    def open(self):

        self.index = 0

        super().open()


    # -------------------------
    # Page information
    # -------------------------

    def page_count(self):

        return (
            len(self.items)
            + self.ITEMS_PER_PAGE
            - 1
        ) // self.ITEMS_PER_PAGE


    def current_page(self):

        return self.index // self.ITEMS_PER_PAGE


    def page_text(self):

        return "{}/{}".format(

            self.current_page() + 1,

            self.page_count()

        )


    # -------------------------
    # Navigation
    # -------------------------

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


    def previous_page(self):

        if self.current_page() == 0:

            return

        self.index = (

            (self.current_page() - 1)

            * self.ITEMS_PER_PAGE

        )

        self.draw()


    def next_page(self):

        if self.current_page() >= self.page_count() - 1:

            return

        self.index = (

            (self.current_page() + 1)

            * self.ITEMS_PER_PAGE

        )

        self.draw()


    # -------------------------
    # Buttons
    # -------------------------

    def update(self, event):

        if event == "UP":

            self.up()


        elif event == "DOWN":

            self.down()


        elif event == "UP_REPEAT":

            self.previous_page()


        elif event == "DOWN_REPEAT":

            self.next_page()


        elif event == "SELECT":

            return self.select()


        return None


    # -------------------------
    # Selection
    # -------------------------

    def select(self):

        selected = self.items[self.index]

        print("Learan:", selected)

        # -------------------------
        # Return to main menu
        # -------------------------

        if selected == "Back":

            return self.parent


        # -------------------------
        # Practice modes
        # -------------------------

        if selected == "Single Character":

            print("Starting Single Character practice")
            
            return "single_character"

        elif selected == "Character Groups":

            return "random_group"


        elif selected == "Random Words":

            return "random_words"


        elif selected == "Callsigns":

            print("Callsigns coming soon")


        elif selected == "Prosigns":

            print("Prosigns coming soon")


        elif selected == "Q-Codes":

            print("Q-Codes coming soon")


        elif selected == "Mixed Text":

            print("Mixed Text coming soon")


        elif selected == "Game":

            print("Game coming soon")

        return None


    # -------------------------
    # Draw
    # -------------------------

    def draw(self):

        self.display.show_menu(

            self.title,

            self.items,

            self.index,

            self.current_page(),

            self.ITEMS_PER_PAGE,

            self.page_text()

        )

        self.display.show_softkeys(

            "SELECT",

            "DOWN",

            "UP"

        )


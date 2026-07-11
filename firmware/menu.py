from screen import Screen


class Menu(Screen):

    # -------------------------
    # Menu layout
    # -------------------------

    # Maximum number of menu items shown
    # on one display page.
    ITEMS_PER_PAGE = 5


    def __init__(self, display):

        super().__init__()

        self.display = display


        # -------------------------
        # Main menu
        # -------------------------

        self.main_items = [
            "Practice",
            "Settings",
            "Keyer Mode",
            "About"
        ]


        # -------------------------
        # Keyer mode menu
        # -------------------------

        self.keyer_items = [
            "Straight",
            "Bug",
            "Iambic A",
            "Iambic B",
            "Back"
        ]


        # -------------------------
        # Current menu state
        # -------------------------

        self.items = self.main_items

        self.index = 0

        self.screen = "main"

        self.title = "MAIN MENU"


    def open(self):

        # -------------------------
        # Return to main menu
        # -------------------------

        self.screen = "main"

        self.title = "MAIN MENU"

        self.items = self.main_items

        self.index = 0

        self.draw()


    # -------------------------
    # Page information
    # -------------------------

    def page_count(self):

        """
        Return the total number of pages
        needed for the current menu.
        """

        count = len(self.items)

        pages = (
            count + self.ITEMS_PER_PAGE - 1
        ) // self.ITEMS_PER_PAGE

        # A menu should always have at least
        # one page, even if it is temporarily empty.
        if pages < 1:

            pages = 1

        return pages


    def current_page(self):

        """
        Return the current zero-based page number.

        Page 1 is returned as 0.
        Page 2 is returned as 1.
        """

        return self.index // self.ITEMS_PER_PAGE


    def page_text(self):

        """
        Return text shown in the corner,
        for example:

            1/1
            1/2
            2/2
        """

        return "{}/{}".format(
            self.current_page() + 1,
            self.page_count()
        )


    # -------------------------
    # Item navigation
    # -------------------------

    def up(self, amount=1):

        self.index -= amount

        # Wrap from the first item
        # to the last item.
        while self.index < 0:

            self.index += len(self.items)

        self.draw()


    def down(self, amount=1):

        self.index += amount

        # Wrap from the last item
        # to the first item.
        while self.index >= len(self.items):

            self.index -= len(self.items)

        self.draw()


    # -------------------------
    # Page navigation
    # -------------------------

    # -------------------------
    # Previous menu page
    # -------------------------

    def previous_page(self):

        current_page = self.current_page()

        # Already on the first page.
        # Ignore further hold events.
        if current_page <= 0:

            return

        previous_page = current_page - 1

        self.index = (
            previous_page
            * self.ITEMS_PER_PAGE
        )

        self.draw()


    # -------------------------
    # Next menu page
    # -------------------------

    def next_page(self):

        current_page = self.current_page()

        last_page = self.page_count() - 1

        # Already on the last page.
        # Ignore further hold events.
        if current_page >= last_page:

            return

        next_page = current_page + 1

        self.index = (
            next_page
            * self.ITEMS_PER_PAGE
        )

        self.draw()


    # -------------------------
    # Button events
    # -------------------------

    def update(self, event):

        if event == "UP":

            self.up()


        elif event == "DOWN":

            self.down()


        elif event == "SELECT":

            return self.select()


        elif event == "UP_REPEAT":

            self.previous_page()


        elif event == "DOWN_REPEAT":

            self.next_page()


        elif event == "SELECT_REPEAT":

            # Reserved for future use.
            # Holding Select currently does nothing.
            pass


        return None


    # -------------------------
    # Select current item
    # -------------------------

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
    # KEYER MODE
    # -------------------------

        elif self.screen == "keyer":

            if selected == "Back":

                self.open()

                return None

            print("Mode:", selected)


        self.draw()

        return None


    # -------------------------
    # Draw menu
    # -------------------------

    def draw(self):

        page = self.current_page()

        page_text = self.page_text()


        # -------------------------
        # New display interface
        # -------------------------
        #
        # We will update display.py next so that
        # show_menu() accepts page and page_text.
        #
        # The fallback keeps this menu compatible
        # with the current display.py until then.
        # -------------------------

        try:

            self.display.show_menu(
                self.title,
                self.items,
                self.index,
                page,
                self.ITEMS_PER_PAGE,
                page_text
            )

        except TypeError:

            self.display.show_menu(
                self.title,
                self.items,
                self.index
            )
class Screen:

    def __init__(self):

        # -------------------------
        # Navigation
        # -------------------------

        # Screen to return to after Confirm,
        # Back, Exit, or Cancel.
        self.parent = None


        # -------------------------
        # Soft-key short actions
        # -------------------------
        #
        # These are ordered by physical position:
        #
        #     left, centre, right
        # -------------------------

        self.softkeys = (
            "",
            "",
            ""
        )


        # -------------------------
        # Soft-key hold actions
        # -------------------------
        #
        # These describe what happens when each
        # physical button is held.
        #
        # Examples:
        #
        #     Cancel, -5, +5
        #     Page, Up, Down
        # -------------------------

        self.hold_keys = (
            "",
            "",
            ""
        )


    # -------------------------
    # Open screen
    # -------------------------

    def open(self):

        # Some screens may temporarily have no
        # display assigned.
        if hasattr(self, "display"):

            self.display.clear()

        self.draw()

    # -------------------------
    # Handle button event
    # -------------------------

    def update(self, event):

        return None


    # -------------------------
    # Set soft-key labels
    # -------------------------

    def set_softkeys(
        self,
        left,
        centre,
        right,
        hold_left="",
        hold_centre="",
        hold_right=""
    ):

        self.softkeys = (
            left,
            centre,
            right
        )

        self.hold_keys = (
            hold_left,
            hold_centre,
            hold_right
        )


    # -------------------------
    # Draw soft-key labels
    # -------------------------

    def draw_softkeys(self):

        # Some screens may temporarily have no
        # display assigned.
        if not hasattr(self, "display"):

            return


        left, centre, right = self.softkeys

        hold_left, hold_centre, hold_right = (
            self.hold_keys
        )


        # -------------------------
        # New display interface
        # -------------------------
        #
        # The new version supports both short
        # and hold labels.
        # -------------------------

        try:

            self.display.show_softkeys(
                left,
                centre,
                right,
                hold_left,
                hold_centre,
                hold_right
            )


        # -------------------------
        # Compatibility fallback
        # -------------------------
        #
        # Until display.py is updated, show only
        # the original three short labels.
        # -------------------------

        except TypeError:

            self.display.show_softkeys(
                left,
                centre,
                right
            )

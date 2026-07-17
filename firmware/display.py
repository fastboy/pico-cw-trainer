from machine import Pin, SPI
import st7789
import theme
import vga1_16x16 as font


class Display:

    # -------------------------
    # Display dimensions
    # -------------------------
    #
    # Rotation 1 makes the physical
    # 240 x 320 display appear as:
    #
    #     width  = 320
    #     height = 240
    # -------------------------

    WIDTH = 320
    HEIGHT = 240

    def __init__(self):

        self.font = font


        # -------------------------
        # Backlight
        # -------------------------

        bl = Pin(
            22,
            Pin.OUT
        )

        bl.value(1)


        # -------------------------
        # SPI
        # -------------------------

        spi = SPI(
            0,
            baudrate=40000000,
            polarity=0,
            phase=0,
            sck=Pin(18),
            mosi=Pin(19),
        )


        # -------------------------
        # Text history
        # -------------------------

        self.lines = [
            "",
            "",
            "",
            ""
        ]


        # -------------------------
        # TFT
        # -------------------------

        self.tft = st7789.ST7789(
            spi,
            240,
            320,
            reset=Pin(20, Pin.OUT),
            dc=Pin(21, Pin.OUT),
            cs=Pin(17, Pin.OUT),
            backlight=bl,
            rotation=1,
            color_order=st7789.BGR,
        )


        self.tft.inversion_mode(False)
        self.tft.fill(
            theme.BACKGROUND
        )
    # -------------------------
    # Main title
    # -------------------------

    def clear(self):

        self.tft.fill(0)
        
    def title(self):

        self.tft.text(
            self.font,
            "CW TRAINER",
            10,
            10,
            theme.TITLE
        )


    # -------------------------
    # Current Morse pattern
    # -------------------------

    def show_pattern(self, pattern):

        # Clear the complete input area before
        # drawing the next character's pattern.
        #
        # This removes:
        # - the previous completed pattern
        # - the previous decoded letter
        # - any overflow from a very long pattern
        self.tft.fill_rect(
            0,
            45,
            self.WIDTH,
            47,
            theme.BACKGROUND
        )

        if pattern:

            self.tft.text(
                self.font,
                pattern,
                10,
                45,
                theme.PATTERN
            )


    # -------------------------
    # Menu
    # -------------------------

    def show_menu(
        self,
        title,
        items,
        selected,
        page=0,
        items_per_page=5,
        page_text="1/1"
    ):

        # -------------------------
        # Clear whole screen
        # -------------------------

        self.tft.fill(
            st7789.BLACK
        )


        # -------------------------
        # Menu title
        # -------------------------

        self.tft.text(
            self.font,
            title,
            40,
            10,
            theme.TITLE
        )


        # -------------------------
        # Page indicator
        # -------------------------
        #
        # The font is 16 pixels wide.
        # This calculates the text width
        # and places it near the right edge.
        #
        # Examples:
        #
        #     1/1
        #     1/2
        #     2/2
        # -------------------------

        page_width = len(page_text) * 16

        page_x = (
            self.WIDTH
            - page_width
            - 8
        )

        self.tft.text(
            self.font,
            page_text,
            page_x,
            10,
            theme.TOP_INDICATOR
        )


        # -------------------------
        # Current page range
        # -------------------------
        #
        # Page 0:
        #
        #     items 0 to 4
        #
        # Page 1:
        #
        #     items 5 to 9
        # -------------------------

        first_item = (
            page * items_per_page
        )

        last_item = (
            first_item
            + items_per_page
        )


        # -------------------------
        # Visible menu items
        # -------------------------

        visible_items = items[
            first_item:last_item
        ]


        # -------------------------
        # Draw menu items
        # -------------------------

        y = 50

        for local_index, item in enumerate(
            visible_items
        ):

            # Convert the position on this page
            # back into the full menu index.
            item_index = (
                first_item
                + local_index
            )


            if item_index == selected:

                text = "> " + item

                color = theme.MENU_SELECTED

            else:

                text = "  " + item

                color = theme.MENU_NORMAL


            self.tft.text(
                self.font,
                text,
                24,
                y,
                color
            )

            y += 28


    # -------------------------
    # Decoded letter
    # -------------------------

    def show_letter(self, letter):

        self.tft.fill_rect(
            0,
            70,
            self.WIDTH,
            22,
            theme.BACKGROUND
        )

        if letter:

            x = (
                self.WIDTH - 16
            ) // 2

            self.tft.text(
                self.font,
                letter,
                x,
                70,
                theme.LABEL
            )

    # -------------------------
    # Current speed
    # -------------------------

    def show_speed(self, wpm):

        self.tft.fill_rect(
            230,
            10,
            90,
            20,
            theme.BACKGROUND
        )

        text = (
            "WPM "
            + str(wpm)
        )

        self.tft.text(
            self.font,
            text,
            200,
            10,
            theme.TOP_INDICATOR
        )

    # -------------------------
    # Decoded text area
    # -------------------------

    def show_text(self, text):

        # -------------------------
        # Text area
        # -------------------------

        x = 8
        y = 110

        line_height = 25

        max_chars = 19
        max_lines = 4


        # -------------------------
        # Wrap text by words
        # -------------------------

        lines = []

        current_line = ""


        for word in text.split(" "):

            # Preserve a pending word gap without
            # creating multiple empty lines.
            if not word:

                continue


            if not current_line:

                # Split unusually long words
                while len(word) > max_chars:

                    lines.append(
                        word[:max_chars]
                    )

                    word = word[max_chars:]


                current_line = word


            elif (
                len(current_line)
                + 1
                + len(word)
                <= max_chars
            ):

                current_line += " " + word


            else:

                lines.append(
                    current_line
                )

                while len(word) > max_chars:

                    lines.append(
                        word[:max_chars]
                    )

                    word = word[max_chars:]

                current_line = word


        if current_line:

            lines.append(
                current_line
            )


        # Keep only the newest visible lines
        lines = lines[-max_lines:]


        # -------------------------
        # Clear old text
        # -------------------------

        self.tft.fill_rect(

            0,

            101,

            self.WIDTH,

            119,

            theme.BACKGROUND
        )


        # -------------------------
        # Draw complete text
        # -------------------------

        for line in lines:

            self.tft.text(

                self.font,

                line,

                x,

                y,

                theme.TEXT
            )

            y += line_height


    # -------------------------
    # Soft-key labels
    # -------------------------
    #
    # These labels describe the short-press
    # action of the three physical buttons.
    #
    # Later we can add a second, smaller row
    # for hold actions such as:
    #
    #     +5
    #     Cancel
    #     Page +
    # -------------------------

    def show_softkeys(
        self,
        left,
        center,
        right
    ):

        # Accept both formats:
        #
        # Old:
        #     "BACK"
        #
        # New:
        #     ("HELP", "HINT")
        #
        # Tuple order:
        #     (hold_label, press_label)

        def split_labels(value):

            if isinstance(value, tuple):

                return value

            return "", value


        def draw_centered(
            text,
            centre,
            y,
            color
        ):

            if not text:

                return

            text_width = (
                len(text) * 16
            )

            x = centre - (
                text_width // 2
            )

            self.tft.text(
                self.font,
                text,
                x,
                y,
                color
            )


        left_top, left_bottom = (
            split_labels(left)
        )

        center_top, center_bottom = (
            split_labels(center)
        )

        right_top, right_bottom = (
            split_labels(right)
        )


        top_labels = (
            left_top,
            center_top,
            right_top
        )

        bottom_labels = (
            left_bottom,
            center_bottom,
            right_bottom
        )


        button_centres = (
            40,
            160,
            280
        )


        # Clear the normal soft-key row.
        self.tft.fill_rect(
            0,
            221,
            self.WIDTH,
            19,
            theme.BACKGROUND
        )


        # Clear any previous hold labels.
        previous_top_labels = getattr(
            self,
            "_softkey_top_labels",
            ("", "", "")
        )


        for index in range(3):

            if (
                previous_top_labels[index]
                or top_labels[index]
            ):

                centre = (
                    button_centres[index]
                )

                self.tft.fill_rect(
                    centre - 40,
                    204,
                    80,
                    16,
                    theme.BACKGROUND
                )


        self._softkey_top_labels = (
            top_labels
        )


        # Draw hold labels above divider.
        for index in range(3):

            draw_centered(
                top_labels[index],
                button_centres[index],
                204,
                theme.SOFT_BUTTON
            )


        # Draw press labels below divider.
        for index in range(3):

            draw_centered(
                bottom_labels[index],
                button_centres[index],
                223,
                theme.SOFT_BUTTON
            )

    # -------------------------
    # divider
    # -------------------------   
    def divider(self, y, color=theme.DIVIDER):

        self.tft.hline(
            0,
            y,
            self.WIDTH,
            color
        )









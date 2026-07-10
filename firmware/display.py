from machine import Pin, SPI
import st7789
import vga1_16x16 as font


class Display:

    def __init__(self):

        self.font = font
        
        bl = Pin(22, Pin.OUT)
        bl.value(1)

        spi = SPI(
            0,
            baudrate=40000000,
            polarity=0,
            phase=0,
            sck=Pin(18),
            mosi=Pin(19),
        )
        self.lines = [
                "",
                "",
                "",
                ""
            ]

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

        self.tft.fill(st7789.BLACK)


    def title(self):

        self.tft.text(
            font,
            "CW TRAINER",
            70,
            10,
            st7789.YELLOW
        )


    def show_pattern(self, pattern):

        self.tft.fill_rect(
            10,
            45,
            90,
            25,
            st7789.BLACK
        )

        self.tft.text(
            font,
            pattern,
            10,
            45,
            st7789.WHITE
        )

    def show_menu(self, title, items, selected):

        # clear whole screen
        self.tft.fill(st7789.BLACK)


        # title
        self.tft.text(
            font,
            title,
            80,
            10,
            st7789.YELLOW
        )


        # menu items
        y = 50

        for i, item in enumerate(items):

            if i == selected:
                text = "> " + item
                color = st7789.GREEN

            else:
                text = "  " + item
                color = st7789.WHITE


            self.tft.text(
                font,
                text,
                40,
                y,
                color
            )

            y += 25

    def show_letter(self, letter):

        self.tft.fill_rect(
            120,
            45,
            40,
            25,
            st7789.BLACK
        )

        self.tft.text(
            font,
            letter,
            120,
            45,
            st7789.GREEN
        )

    def show_speed(self, wpm):

        self.tft.fill_rect(
            180,
            45,
            80,
            25,
            st7789.BLACK
        )

        text = "WPM " + str(wpm)

        self.tft.text(
            font,
            text,
            180,
            45,
            st7789.CYAN
        )


    def show_text(self, text):

        self.lines[-1] += text

        if len(self.lines[-1]) > 26:

            self.lines.append("")
            self.lines.pop(0)

        self.tft.fill_rect(
            0,
            85,
            240,
            150,
            st7789.BLACK
        )

        y = 90

        for line in self.lines:

            self.tft.text(
                font,
                line,
                10,
                y,
                st7789.WHITE
            )

            y += 25
    def show_softkeys(self, left, center, right):

        # clear bottom line
        self.tft.fill_rect(
            0,
            210,
            320,
            30,
            st7789.BLACK
        )

        self.tft.text(
            font,
            left,
            10,
            215,
            st7789.WHITE
        )

        self.tft.text(
            font,
            center,
            135,
            215,
            st7789.WHITE
        )

        self.tft.text(
            font,
            right,
            260,
            215,
            st7789.WHITE
        )


from machine import Pin, SPI
import st7789
import vga1_16x16 as font


class Display:

    def __init__(self):

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

        self.tft = st7789.ST7789(
            spi,
            240,
            320,
            reset=Pin(20, Pin.OUT),
            dc=Pin(21, Pin.OUT),
            cs=Pin(17, Pin.OUT),
            backlight=bl,
            rotation=0,
        )

        self.tft.fill(st7789.BLACK)


    def title(self):

        self.tft.text(
            font,
            "CW TRAINER",
            30,
            20,
            st7789.YELLOW
        )


    def show_pattern(self, pattern):

        self.tft.fill_rect(
            20,
            70,
            220,
            30,
            st7789.BLACK
        )

        self.tft.text(
            font,
            pattern,
            30,
            70,
            st7789.WHITE
        )


    def show_letter(self, letter):

        self.tft.fill_rect(
            20,
            120,
            220,
            40,
            st7789.BLACK
        )

        self.tft.text(
            font,
            letter,
            30,
            120,
            st7789.GREEN
        )


    def show_speed(self, wpm):

        self.tft.fill_rect(
            20,
            180,
            220,
            30,
            st7789.BLACK
        )

        text = "WPM " + str(wpm)

        self.tft.text(
            font,
            text,
            30,
            180,
            st7789.CYAN
        )
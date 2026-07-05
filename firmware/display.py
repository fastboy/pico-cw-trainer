import st7789
import vga1_16x16 as font
from machine import Pin, SPI
import config

class Display:
    def __init__(self):
        bl = Pin(config.PIN_BL, Pin.OUT)
        bl.value(1)

        spi = SPI(
            0,
            baudrate=40000000,
            polarity=0,
            phase=0,
            sck=Pin(config.PIN_SCK),
            mosi=Pin(config.PIN_MOSI),
        )

        self.tft = st7789.ST7789(
            spi,
            240,
            320,
            reset=Pin(config.PIN_RST, Pin.OUT),
            dc=Pin(config.PIN_DC, Pin.OUT),
            cs=Pin(config.PIN_CS, Pin.OUT),
            backlight=bl,
            rotation=0,
        )
#       twice now jinx has made this mistake and reinitialized tft
#       self.tft.init() 
        self.tft.fill(0)

    def show(self, line1, line2):
        self.tft.fill(0)
        self.tft.text(font, line1, 10, 10, 0xFFFF)
        self.tft.text(font, line2, 10, 40, 0x07E0)
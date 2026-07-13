from display import Display
import st7789
import time


display = Display()
tft = display.tft


# -------------------------------------------------
# Basic labelled palette
# -------------------------------------------------
#
# Layout:
#
# RED     GREEN   BLUE    YELLOW
# CYAN    MAGENTA WHITE   BLACK
#
# Then darker versions underneath.
# -------------------------------------------------

colors = [

    # Bright colours
    ("RED",     255,   0,   0),
    ("GREEN",     0, 255,   0),
    ("BLUE",      0,   0, 255),
    ("YELLOW",  255, 255,   0),

    ("CYAN",      0, 255, 255),
    ("MAGENTA", 255,   0, 255),
    ("WHITE",   255, 255, 255),
    ("BLACK",     0,   0,   0),

    # Darker colours
    ("DARK RED",    128,   0,   0),
    ("DARK GREEN",    0, 128,   0),
    ("DARK BLUE",     0,   0, 128),
    ("OLIVE",       128, 128,   0),

    ("TEAL",          0, 128, 128),
    ("PURPLE",      128,   0, 128),
    ("GREY",        128, 128, 128),
    ("DARK GREY",    48,  48,  48),
]


BLOCK_WIDTH = 80
BLOCK_HEIGHT = 60


tft.fill(st7789.BLACK)


for index, item in enumerate(colors):

    name, red, green, blue = item

    column = index % 4
    row = index // 4

    x = column * BLOCK_WIDTH
    y = row * BLOCK_HEIGHT

    color = st7789.color565(
        red,
        green,
        blue
    )

    tft.fill_rect(
        x,
        y,
        BLOCK_WIDTH,
        BLOCK_HEIGHT,
        color
    )


while True:

    time.sleep(1)

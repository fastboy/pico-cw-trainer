from display import Display

import theme
import time


display = Display()
tft = display.tft
font = display.font


# -------------------------------------------------
# Worst-case sample content
# -------------------------------------------------

TARGET_WORD = "CHERRY"

HINT_LINES = [
    "-.-. .... . .-.",
    ".-. -.--",
    "----- ----- -----"
]

SENT_TEXT_LINES = [
    "CHERR?",
    "EXTRA TEXT"
]

SENT_PATTERN_LINES = [
    "-.-. .... . .-. .-.",
    "-.-- ----- -----"
]


# -------------------------------------------------
# Clear screen
# -------------------------------------------------

display.clear()


# -------------------------------------------------
# Top bar
# -------------------------------------------------

display.title()

display.show_speed(
    60
)

display.divider(
    38
)


# -------------------------------------------------
# Target section
# -------------------------------------------------

tft.text(
    font,
    "SEND WORD",
    10,
    42,
    theme.LABEL
)

tft.text(
    font,
    TARGET_WORD,
    10,
    60,
    theme.TARGET
)


hint_y = 78

for line in HINT_LINES:

    tft.text(
        font,
        line,
        10,
        hint_y,
        theme.HINT
    )

    hint_y += 18


display.divider(
    132
)


# -------------------------------------------------
# User input heading and result
# -------------------------------------------------

tft.text(
    font,
    "YOU SENT",
    10,
    136,
    theme.LABEL
)

tft.text(
    font,
    "INCORRECT",
    170,
    136,
    theme.ERROR
)


# -------------------------------------------------
# Decoded input
# -------------------------------------------------

text_y = 154

for line in SENT_TEXT_LINES:

    tft.text(
        font,
        line,
        10,
        text_y,
        theme.INPUT
    )

    text_y += 18


# -------------------------------------------------
# Morse input
# -------------------------------------------------

pattern_y = 188

for line in SENT_PATTERN_LINES:

    tft.text(
        font,
        line,
        10,
        pattern_y,
        theme.PATTERN
    )

    pattern_y += 17


# -------------------------------------------------
# Bottom divider
# -------------------------------------------------

display.divider(
    220
)


# -------------------------------------------------
# Soft buttons
# -------------------------------------------------
#
# Drawn manually because the current show_softkeys()
# places its text at y = 216. For this proposed layout,
# y = 223 gives the content above a little more room.
# -------------------------------------------------

tft.text(
    font,
    "BACK",
    8,
    223,
    theme.SOFT_BUTTON
)

tft.text(
    font,
    " NEXT",
    120,
    223,
    theme.SOFT_BUTTON
)

tft.text(
    font,
    " HINT",
    232,
    223,
    theme.SOFT_BUTTON
)


while True:

    time.sleep(1)

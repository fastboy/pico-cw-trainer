from machine import Pin, SPI, PWM
import st7789
import vga1_16x16 as font
import time

# -----------------------------
# TFT
# -----------------------------
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

display = st7789.ST7789(
    spi,
    240,
    320,
    reset=Pin(20, Pin.OUT),
    dc=Pin(21, Pin.OUT),
    cs=Pin(17, Pin.OUT),
    backlight=bl,
    rotation=0,
)

display.fill(st7789.BLACK)

# -----------------------------
# Buttons
# -----------------------------
dot = Pin(2, Pin.IN, Pin.PULL_UP)
dash = Pin(3, Pin.IN, Pin.PULL_UP)

# -----------------------------
# Speaker
# -----------------------------
speaker = PWM(Pin(4))
speaker.freq(650)
speaker.duty_u16(0)

# -----------------------------
# Morse decoder
# -----------------------------
morse = {
    ".":"E",
    "-":"T",
    ".-":"A",
    "-.":"N",
    "..":"I",
    "--":"M",
    "...":"S",
    "---":"O",
}

buffer = ""
last_press = time.ticks_ms()

display.text(font, "CW TEST", 40, 20, st7789.YELLOW)

while True:

    changed = False

    if not dot.value():

        speaker.duty_u16(30000)

        display.fill_rect(20,60,200,30,st7789.BLACK)
        display.text(font,"DIT",20,60,st7789.GREEN)

        while not dot.value():
            pass

        speaker.duty_u16(0)

        buffer += "."
        changed = True

    elif not dash.value():

        speaker.duty_u16(30000)

        display.fill_rect(20,60,200,30,st7789.BLACK)
        display.text(font,"DAH",20,60,st7789.CYAN)

        while not dash.value():
            pass

        speaker.duty_u16(0)

        buffer += "-"
        changed = True

    if changed:

        last_press = time.ticks_ms()

        display.fill_rect(20,100,200,30,st7789.BLACK)
        display.text(font,buffer,20,100,st7789.WHITE)

        display.fill_rect(20,140,200,30,st7789.BLACK)

    # decode after 1 second pause

    if buffer and time.ticks_diff(time.ticks_ms(), last_press) > 1000:

        letter = morse.get(buffer,"?")

        display.text(font,letter,20,140,st7789.YELLOW)

        print(buffer,"=",letter)

        buffer = ""

    time.sleep_ms(10)
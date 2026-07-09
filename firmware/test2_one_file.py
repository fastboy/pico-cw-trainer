from machine import Pin, PWM, SPI
import st7789
import vga1_16x16 as font
import time

# ----------------------------
# CONFIG
# ----------------------------
WPM = 12
UNIT = 1200 // WPM   # ms per dit

FREQ = 650

# ----------------------------
# TFT SETUP
# ----------------------------
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

# ----------------------------
# INPUTS
# ----------------------------
dot = Pin(2, Pin.IN, Pin.PULL_UP)
dash = Pin(3, Pin.IN, Pin.PULL_UP)

# ----------------------------
# AUDIO
# ----------------------------
spk = PWM(Pin(4))
spk.freq(FREQ)
spk.duty_u16(0)

def tone(on):
    spk.duty_u16(30000 if on else 0)

def beep(duration_ms):
    tone(True)
    time.sleep_ms(duration_ms)
    tone(False)
    time.sleep_ms(UNIT)

# ----------------------------
# MORSE TABLE (A-Z)
# ----------------------------
MORSE = {
    ".-":"A", "-...":"B", "-.-.":"C", "-..":"D", ".":"E",
    "..-.":"F", "--.":"G", "....":"H", "..":"I", ".---":"J",
    "-.-":"K", ".-..":"L", "--":"M", "-.":"N", "---":"O",
    ".--.":"P", "--.-":"Q", ".-.":"R", "...":"S", "-":"T",
    "..-":"U", "...-":"V", ".--":"W", "-..-":"X",
    "-.--":"Y", "--..":"Z"
}

# ----------------------------
# STATE
# ----------------------------
buffer = ""
last_input_time = time.ticks_ms()

# ----------------------------
# UI helper
# ----------------------------
def show(line1, line2):
    display.fill_rect(0, 0, 240, 80, st7789.BLACK)
    display.text(font, line1, 10, 10, st7789.YELLOW)
    display.text(font, line2, 10, 40, st7789.GREEN)

show("CW TRAINER", "READY")

# ----------------------------
# MAIN LOOP
# ----------------------------
while True:

    now = time.ticks_ms()

    # ------------------------
    # INPUT DETECTION
    # ------------------------
    if not dot.value():
        beep(UNIT)
        buffer += "."
        last_input_time = now
        show("DOT", buffer)
        while not dot.value():
            pass

    elif not dash.value():
        beep(UNIT * 3)
        buffer += "-"
        last_input_time = now
        show("DAH", buffer)
        while not dash.value():
            pass

    # ------------------------
    # CHARACTER END (pause)
    # ------------------------
    if buffer and time.ticks_diff(now, last_input_time) > 1200:

        letter = MORSE.get(buffer, "?")

        show(buffer, letter)

        print(buffer, "=", letter)

        buffer = ""

    time.sleep_ms(10)
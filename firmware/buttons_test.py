from machine import Pin
import time


# Buttons
up = Pin(7, Pin.IN, Pin.PULL_UP)
down = Pin(8, Pin.IN, Pin.PULL_UP)
select = Pin(9, Pin.IN, Pin.PULL_UP)


print("BUTTON TEST START")


while True:

    if not up.value():
        print("UP")

    if not down.value():
        print("DOWN")

    if not select.value():
        print("SELECT")


    time.sleep_ms(50)

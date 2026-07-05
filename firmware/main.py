import time
import config
from input import Input
from audio import Audio
from display import Display
from keyer import Keyer
import morse

inp = Input()
audio = Audio()
disp = Display()
keyer = Keyer(audio)

disp.show("CW TRAINER", "READY")

while True:

    state = inp.read()

    if state["dit"]:
        keyer.dit()
        disp.show("DIT", keyer.buffer)
        while inp.read()["dit"]:
            pass

    elif state["dah"]:
        keyer.dah()
        disp.show("DAH", keyer.buffer)
        while inp.read()["dah"]:
            pass

    if keyer.ready_to_decode() and keyer.buffer:
        letter = morse.decode(keyer.buffer)
        disp.show(keyer.buffer, letter)
        print(keyer.buffer, "=", letter)
        keyer.buffer = ""

    time.sleep_ms(10)
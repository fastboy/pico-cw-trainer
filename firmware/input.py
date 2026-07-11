from machine import Pin
import time


class Input:

    # -------------------------
    # Button events
    # -------------------------

    UP = "UP"
    DOWN = "DOWN"
    SELECT = "SELECT"

    UP_REPEAT = "UP_REPEAT"
    DOWN_REPEAT = "DOWN_REPEAT"
    SELECT_REPEAT = "SELECT_REPEAT"


    # -------------------------
    # Timing
    # -------------------------

    # Time before the first hold event.
    REPEAT_DELAY = 400

    # Time between later hold events.
    REPEAT_PERIOD = 120


    def __init__(self):

        # -------------------------
        # Physical buttons
        # -------------------------

        self.up = Pin(
            7,
            Pin.IN,
            Pin.PULL_UP
        )

        self.down = Pin(
            8,
            Pin.IN,
            Pin.PULL_UP
        )

        self.select = Pin(
            9,
            Pin.IN,
            Pin.PULL_UP
        )


        # -------------------------
        # Button state
        # -------------------------
        #
        # Each physical button keeps track of:
        #
        # pin          GPIO input
        # pressed      previous physical state
        # press_time   time when button was pressed
        # last_repeat  time when last repeat was sent
        # repeat_event event generated while held
        # -------------------------

        self.buttons = {

            self.UP: {
                "pin": self.up,
                "pressed": False,
                "press_time": 0,
                "last_repeat": 0,
                "repeat_event": self.UP_REPEAT
            },

            self.DOWN: {
                "pin": self.down,
                "pressed": False,
                "press_time": 0,
                "last_repeat": 0,
                "repeat_event": self.DOWN_REPEAT
            },

            self.SELECT: {
                "pin": self.select,
                "pressed": False,
                "press_time": 0,
                "last_repeat": 0,
                "repeat_event": self.SELECT_REPEAT
            }
        }


    def update(self):

        now = time.ticks_ms()


        # -------------------------
        # Scan order
        # -------------------------
        #
        # If several buttons are pressed at exactly
        # the same moment, this order decides which
        # event is returned first.
        # -------------------------

        for name in (
            self.UP,
            self.DOWN,
            self.SELECT
        ):

            button = self.buttons[name]

            is_pressed = not button["pin"].value()


            # -------------------------
            # Button just pressed
            # -------------------------

            if is_pressed and not button["pressed"]:

                button["pressed"] = True

                button["press_time"] = now

                button["last_repeat"] = now

                return name


            # -------------------------
            # Button held
            # -------------------------

            if is_pressed and button["pressed"]:

                held_time = time.ticks_diff(
                    now,
                    button["press_time"]
                )

                if held_time >= self.REPEAT_DELAY:

                    repeat_time = time.ticks_diff(
                        now,
                        button["last_repeat"]
                    )

                    if repeat_time >= self.REPEAT_PERIOD:

                        button["last_repeat"] = now

                        return button["repeat_event"]


            # -------------------------
            # Button released
            # -------------------------

            if not is_pressed and button["pressed"]:

                button["pressed"] = False


        return None


    def is_pressed(self, name):

        """
        Return the current physical state of a button.

        This will later be useful for modes where a
        button behaves like a continuously held paddle,
        instead of an ordinary repeating menu button.
        """

        if name in self.buttons:

            return not self.buttons[name]["pin"].value()

        return False
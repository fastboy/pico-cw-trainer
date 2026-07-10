from machine import Pin
import time


class Input:

    # Events
    UP = "UP"
    DOWN = "DOWN"
    SELECT = "SELECT"

    UP_REPEAT = "UP_REPEAT"
    DOWN_REPEAT = "DOWN_REPEAT"


    # Timing
    REPEAT_DELAY = 700      # ms before first repeat
    REPEAT_PERIOD = 250     # ms between repeats


    def __init__(self):

        # Buttons
        self.up = Pin(7, Pin.IN, Pin.PULL_UP)
        self.down = Pin(8, Pin.IN, Pin.PULL_UP)
        self.select = Pin(9, Pin.IN, Pin.PULL_UP)


        self.buttons = {

            self.UP: {
                "pin": self.up,
                "pressed": False,
                "press_time": 0,
                "last_repeat": 0
            },


            self.DOWN: {
                "pin": self.down,
                "pressed": False,
                "press_time": 0,
                "last_repeat": 0
            },


            self.SELECT: {
                "pin": self.select,
                "pressed": False,
                "press_time": 0,
                "last_repeat": 0
            }
        }


    def update(self):

        now = time.ticks_ms()


        # Fixed order:
        # If multiple buttons are pressed,
        # this order decides priority.
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


                # SELECT never repeats
                if name == self.SELECT:
                    continue


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

                        if name == self.UP:
                            return self.UP_REPEAT

                        if name == self.DOWN:
                            return self.DOWN_REPEAT



            # -------------------------
            # Button released
            # -------------------------
            if not is_pressed and button["pressed"]:

                button["pressed"] = False



        return None



    def is_pressed(self, name):

        """
        Returns current physical state.
        Mainly useful for debugging.
        """

        if name in self.buttons:

            return not self.buttons[name]["pin"].value()

        return False
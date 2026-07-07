import time


class Keyer:

    IDLE = 0
    KEY_DOWN = 1
    KEY_UP = 2


    def __init__(self, wpm=20):

        self.set_speed(wpm)

        self.state = self.IDLE

        self.output = False

        self.next_change = 0

        self.dot_request = False
        self.dash_request = False
        self.dot_held = False
        self.dash_held = False


    def set_speed(self, wpm):

        self.dot = int(1200 / wpm)
        self.dash = self.dot * 3


    def request_dot(self):

        print("DOT REQUEST")
        self.dot_request = True


    def request_dash(self):

        print("DASH REQUEST")
        self.dash_request = True

    def hold_dot(self):

        self.dot_held = True


    def release_dot(self):

        self.dot_held = False
        
    def hold_dash(self):

        self.dash_held = True


    def release_dash(self):

        self.dash_held = False
        
    def send_dot(self):

        print("START DOT")

        self.state = self.KEY_DOWN

        self.output = True

        self.next_change = time.ticks_add(
            time.ticks_ms(),
            self.dot
        )

        print("KEY DOWN")

    def send_dash(self):

        print("START DASH")

        self.state = self.KEY_DOWN

        self.output = True

        self.next_change = time.ticks_add(
            time.ticks_ms(),
            self.dash
        )

        print("KEY DOWN DASH")
        
    def update(self, now):

        if self.state == self.IDLE:

            if self.dot_request:

                self.dot_request = False

                self.send_dot()
            elif self.dash_request:

                self.dash_request = False
                self.send_dash()

            return


        if time.ticks_diff(now, self.next_change) < 0:

            return


        if self.state == self.KEY_DOWN:

            self.output = False

            self.state = self.KEY_UP

            self.next_change = time.ticks_add(
                now,
                self.dot
            )

            print("KEY UP")

            return


        if self.state == self.KEY_UP:

            self.state = self.IDLE

            print("ELEMENT FINISHED")


            if self.dot_held:

                self.request_dot()

            elif self.dash_held:

                self.request_dash()

        return

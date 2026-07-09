import time


class Keyer:

    # States
    IDLE = 0
    KEY_DOWN = 1
    KEY_UP = 2

    # Elements
    DOT = 0
    DASH = 1

    # Modes
    MODE_STRAIGHT = 0
    MODE_BUG = 1
    MODE_IAMBIC_A = 2
    MODE_IAMBIC_B = 3

    def __init__(self, wpm=20):

        self.set_speed(wpm)

        self.state = self.IDLE
        self.output = False
        self.next_change = 0

        self.mode = self.MODE_IAMBIC_A

        # History
        self.first_held = None
        self.last_sent = None

        # Requests
        self.dot_request = False
        self.dash_request = False

        # Paddle states
        self.dot_held = False
        self.dash_held = False


    def set_speed(self, wpm):

        self.dot = int(1200 / wpm)
        self.dash = self.dot * 3


    def set_mode(self, mode):

        self.mode = mode


    def request_dot(self):

        print("DOT REQUEST")
        self.dot_request = True


    def request_dash(self):

        print("DASH REQUEST")
        self.dash_request = True


    def hold_dot(self):

        self.dot_held = True

        if self.first_held is None:
            self.first_held = self.DOT


    def release_dot(self):

        self.dot_held = False

        if not self.dot_held and not self.dash_held:
            self.first_held = None


    def hold_dash(self):

        self.dash_held = True

        if self.first_held is None:
            self.first_held = self.DASH


    def release_dash(self):

        self.dash_held = False

        if not self.dot_held and not self.dash_held:
            self.first_held = None


    def send_dot(self):

        self.last_sent = self.DOT

        print("START DOT")

        self.state = self.KEY_DOWN
        self.output = True

        self.next_change = time.ticks_add(
            time.ticks_ms(),
            self.dot
        )

        print("KEY DOWN")


    def send_dash(self):

        self.last_sent = self.DASH

        print("START DASH")

        self.state = self.KEY_DOWN
        self.output = True

        self.next_change = time.ticks_add(
            time.ticks_ms(),
            self.dash
        )

        print("KEY DOWN DASH")


    def handle_straight(self):

        # Straight key does not repeat automatically.
        pass


    def handle_bug(self):

        # Automatic dots only.
        if self.dot_held:
            self.request_dot()


    def handle_iambic_a(self):

        # Currently identical to the original behaviour.
        # Proper alternating will be added later.

        if self.dot_held:

            self.request_dot()

        elif self.dash_held:

            self.request_dash()


    def handle_iambic_b(self):

        # For now identical to Iambic A.
        # Later this will implement element latching.
        self.handle_iambic_a()

    def debug(self):

        print("--------------------------------")
        print("STATE      :", self.state)
        print("MODE       :", self.mode)
        print("DOT HELD   :", self.dot_held)
        print("DASH HELD  :", self.dash_held)
        print("FIRST HELD :", self.first_held)
        print("LAST SENT  :", self.last_sent)
        print("OUTPUT     :", self.output)

    def update(self, now):

        if self.state == self.IDLE:

            if self.dot_request:
                self.dot_request = False
                self.send_dot()

            elif self.dash_request:
                self.dash_request = False
                self.send_dash()

            elif self.dot_held:
                self.send_dot()

            elif self.dash_held:
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

            if self.mode == self.MODE_STRAIGHT:

                self.handle_straight()

            elif self.mode == self.MODE_BUG:

                self.handle_bug()

            elif self.mode == self.MODE_IAMBIC_A:

                self.handle_iambic_a()

            elif self.mode == self.MODE_IAMBIC_B:

                self.handle_iambic_b()

        return
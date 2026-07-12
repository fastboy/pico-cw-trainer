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

    def __init__(self, wpm=12):

        self.set_speed(wpm)

        self.state = self.IDLE
        self.output = False
        self.next_change = 0

        # Completed elements waiting for decoder
        self.events = []

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

        self.wpm = wpm

        self.dot = int(1200 / wpm)
        self.dash = self.dot * 3


    def set_mode(self, mode):

        self.mode = mode


    def request_dot(self):

        self.dot_request = True


    def request_dash(self):

        self.dash_request = True


    def hold_dot(self):

        if not self.dot_held:
            self.request_dot()

        self.dot_held = True


    def release_dot(self):

        self.dot_held = False

        if not self.dot_held and not self.dash_held:
            self.first_held = None


    def hold_dash(self):

        if not self.dash_held:
            self.request_dash()

        self.dash_held = True


    def release_dash(self):

        self.dash_held = False

        if not self.dot_held and not self.dash_held:
            self.first_held = None


    def send_dot(self):

        self.last_sent = self.DOT

        # Report the dot immediately
        self.events.append(self.DOT)

        self.state = self.KEY_DOWN
        self.output = True

        self.next_change = time.ticks_add(
            time.ticks_ms(),
            self.dot
        )


    def send_dash(self):

        self.last_sent = self.DASH

        # Report the dash immediately
        self.events.append(self.DASH)

        self.state = self.KEY_DOWN
        self.output = True

        self.next_change = time.ticks_add(
            time.ticks_ms(),
            self.dash
        )


    def handle_straight(self):

        # Straight-key handling can be expanded later.
        pass


    def handle_bug(self):

        # Automatic dots only.
        if self.dot_held:
            self.request_dot()


    def handle_iambic_a(self):

        # Paddle handling happens directly in update().
        pass


    def handle_iambic_b(self):

        # Iambic B can be expanded later.
        pass


    def get_events(self):

        events = self.events[:]
        self.events.clear()

        return events


    def debug(self):

        print("--------------------------------")
        print("STATE          :", self.state)
        print("MODE           :", self.mode)
        print("DOT HELD       :", self.dot_held)
        print("DASH HELD      :", self.dash_held)
        print("FIRST HELD     :", self.first_held)
        print("LAST SENT      :", self.last_sent)
        print("OUTPUT         :", self.output)
        print("WPM            :", self.wpm)
        print("DOT LENGTH     :", self.dot)
        print("DASH LENGTH    :", self.dash)


    def update(self, now):

        # -----------------------------
        # Start next element
        # -----------------------------

        if self.state == self.IDLE:

            if self.dot_request:

                self.dot_request = False
                self.send_dot()


            elif self.dash_request:

                self.dash_request = False
                self.send_dash()


            elif self.dot_held and self.dash_held:

                # Alternate while both paddles are held.
                if self.last_sent == self.DASH:
                    self.send_dot()
                else:
                    self.send_dash()


            elif self.dot_held:

                self.send_dot()


            elif self.dash_held:

                self.send_dash()

            return


        # Wait until the current timing period has finished.
        if time.ticks_diff(now, self.next_change) < 0:
            return


        # -----------------------------
        # Tone has finished
        # -----------------------------

        if self.state == self.KEY_DOWN:

            self.output = False

            self.state = self.KEY_UP

            # One-dot silence between Morse elements.
            self.next_change = time.ticks_add(
                now,
                self.dot
            )

            return


        # -----------------------------
        # Inter-element gap finished
        # -----------------------------

        if self.state == self.KEY_UP:

            self.state = self.IDLE

            if self.mode == self.MODE_STRAIGHT:

                self.handle_straight()


            elif self.mode == self.MODE_BUG:

                self.handle_bug()


            elif self.mode == self.MODE_IAMBIC_A:

                self.handle_iambic_a()


            elif self.mode == self.MODE_IAMBIC_B:

                self.handle_iambic_b()

            return

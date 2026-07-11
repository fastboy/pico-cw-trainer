# GPIO Map – Pico CW Trainer

## Display (ST7789)
- SCK  → GP18
- MOSI → GP19
- CS   → GP17
- DC   → GP21
- RST  → GP20
- BL   → GP22

## Inputs
- DIT button / paddle → GP2
- DAH button / paddle → GP3

## Audio
- PWM output → GP4 → BC337 → speaker

## Notes
- All inputs use internal pull-ups
- Active LOW buttons

My current pin usage:

GP2   DOT paddle
GP3   DASH paddle
GP4   Speaker PWM

GP7   Button UP
GP8   Button DOWN
GP9   Button SELECT

GP17  TFT CS
GP18  TFT SCK
GP19  TFT MOSI
GP20  TFT RESET
GP21  TFT DC
GP22  TFT Backlight

So free GPIOs are available.

For the three buttons, I suggest:

Button 1 (UP)      → GP7
Button 2 (DOWN)    → GP8
Button 3 (SELECT)  → GP9

Wiring:

Pico GP7  -------- button -------- GND
Pico GP8  -------- button -------- GND
Pico GP9  -------- button -------- GND
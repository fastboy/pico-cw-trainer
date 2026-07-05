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
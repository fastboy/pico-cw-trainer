# Pico CW Trainer

A portable Raspberry Pi Pico based Morse code trainer, keyer and decoder designed for amateur radio operators.

> **Status:** 🚧 Early development

---

## Project Goals

Build an open-source handheld CW device that can:

- Decode Morse code from a paddle
- Practice sending with an iambic paddle
- Generate adjustable sidetone
- Display decoded characters on a 2.8" TFT display
- Run from an internal Li-ion battery
- Be easy to build using commonly available parts

Long-term goals include:

- Koch training
- Callsign practice
- Random word training
- Memory keyer
- Audio decoding from a radio receiver
- Battery monitoring
- USB firmware updates
- 3D printable enclosure

---

## Hardware

Current prototype:

| Component | Description |
|-----------|-------------|
| MCU | Raspberry Pi Pico |
| Display | 2.8" ST7789 TFT (240×320 SPI) |
| Audio | 8 Ω speaker + BC337 transistor |
| Input | Iambic paddle / push buttons |
| Power | USB (battery support planned) |

---

## Current Progress

- [x] TFT display working
- [x] PWM sidetone working
- [x] Push button input
- [x] Basic Morse decoder
- [ ] Rotary encoder menu
- [ ] Battery management
- [ ] Iambic keyer
- [ ] Audio decoder
- [ ] Portable enclosure

---

## Repository Structure

```
firmware/      MicroPython source code
hardware/      Schematics, wiring and BOM
docs/          Documentation
enclosure/     3D models and STL files
```

---

## License

MIT License

---

## Why?

Commercial CW trainers already exist, but building one from scratch is both educational and rewarding.

This project aims to become a fully featured portable CW trainer that anyone can build, modify and improve.

73!
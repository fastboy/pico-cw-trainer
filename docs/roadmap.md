Menu tree


Main Menu
│
├── Practice
│       ├── xxx
│       ├── xxxx
│       └── xxxx
│
├── Decoder       
│
├── Settings
│       ├── Speed
│       ├── Tone
│       ├── Volume
│       ├── KeyerMode
│       └── Farnsworth
└── About

Screen
│
├── Menu
├── Settings
├── SpeedEditor
├── ToneEditor
├── Practice
├── About
└── Statistics

Responsibility of App

Instead of every test file creating objects, App owns everything:

App
│
├── Display
├── Input
├── Menu
├── Settings
├── Speed
├── Tone
├── Keyer
├── Decoder
├── Practice
│
└── current_screen
App
│
├── Menu
├── Settings
├── Practice
├── Trainer
├── Decoder
├── Character Generator
├── Statistics
└── Config

Files

firmware/
│
├── Core project (keep)
│   ├── keyer.py
│   ├── decoder.py
│   ├── display.py
│   ├── morse.py
│   ├── trainer.py
│   ├── trainer_test.py
│   ├── menu.py
│   ├── input.py
│   ├── config.py
│   ├── hardware.py
│   ├── speaker.py
│   ├── audio.py
│
├── Tests / experiments
│   ├── keyer_test.py
│   ├── speaker_test.py
│   ├── padle_test.py
│   ├── test2_one_file.py
│   ├── backup_workin_monolith.py
│
├── Old versions
│   ├── display_old.py
│   └── mam.py
│
└── Utilities
    └── morse_encoder.py
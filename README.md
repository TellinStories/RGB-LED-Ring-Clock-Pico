## RGB-LED-Ring-Clock-Pico
- A simple RGB LED ring clock built with a Raspberry Pi Pico, WS2812b / NeoPixel ring, and a DS3231 real-time clock module.
- Written in MicroPython and designed as a beginner-friendly hardware project.
- Full instructions will shortly be published on Instructables: https://www.instructables.com/RGB-LED-Ring-Clock/ 
- The as well as 3D printing files are here: https://makerworld.com/en/models/2223262-rgb-led-clock

![IMG_8941](https://github.com/user-attachments/assets/5c5a4834-7761-4bd8-8c6b-71688a9696f7)

## Features
- 12-hour analogue clock display
- Colour-coded minutes
- Automatic hour/minute overlap handling
- Physical daylight-saving time switch

## Code
- clock.py: The main application - a clock
- ds3231.py: Library to interface with the DS3231 module.
- set_time.py: A one-off utility script to set the time on the RTC module.

## Hardware
- Raspberry Pi Pico
- 12-LED WS2812B / NeoPixel ring
- Waveshare Precision RTC Module for Raspberry Pi Pico (DS3231)
- CR1220 battery (sometimes these come included with the RTC module).
- Stripboard / veroboard
- Stranded insulated wire – something around 22 AWG.
- Solid core jumper wire (or use the stranded core wire if that’s all you have).
- 2.54mm Screw terminals – 3 x 2-way terminals or 1 x 2-way and 1x 4-way.
- 2.54mm toggle switch.
- Female USB-C with wires attached.
- Access to a 3D Printer.
- Access to a soldering iron, solder etc.

## Licence
MIT License

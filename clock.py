"""
RGB LED Ring Clock: Main Clock Script

Copyright (c) 2026 John Dovey

Released under the MIT License.
See LICENSE file in the repository for full licence text.
"""

import time
from machine import Pin
from neopixel import NeoPixel
from ds3231 import DS3231

#Use "set time" program to set the time first.

# Constants
Number_neopixels = 12 # We have 12 neopixels in our ring
Offset = 6 # Neopixel 0 is at the bottom and I want it to be at the top, so this is to offset all the neopixelss by 6 positions (e.g. 3pm position to 9pm position)

#Set up I2C (Waveshare Pico RTC DS3231 uses pins 20 and 21)
i2c = machine.I2C(0, scl=machine.Pin(21), sda=machine.Pin(20))
rtc = DS3231(i2c)

# Set up neopixel ring - variable "ring", the pin number (2) and number of neopixels (12)
ring = NeoPixel(Pin(16), Number_neopixels)
ring.fill((0,0,0)) # Clears the ring
ring.write()

# Set up the Daylight Savings Time Switch (optional)
dst_switch = Pin(19, Pin.IN, Pin.PULL_UP)

# Define a simple 12-colour spectrum at 25% brightness
spectrum = [
    (60, 0, 0),     # Red
    (60, 30, 0),    # Orange
    (60, 60, 0),    # Yellow
    (30, 60, 0),    # Yellow-Green
    (0, 60, 0),     # Green
    (0, 60, 30),    # Turquoise
    (0, 60, 60),    # Cyan
    (0, 30, 60),    # Sky Blue
    (0, 0, 60),     # Blue
    (30, 0, 60),    # Violet
    (60, 0, 60),    # Magenta
    (60, 0, 30)     # Pinkish-Red
]

#FUNCTIONS
def clock_position(normal_position):  # This function uses the offset to work out the clock position that needs to light up
    return (normal_position + Offset) % Number_neopixels

def print_info():
    print(f"Time: {hour_24}:{minute:02d}     Hourhand: {hourhand}, Minutehand: {minutehand}") #prints the time, and hour and minute hand positions just to help code

def ring_clear(): #Clears the ring
    ring.fill((0,0,0)) 
    ring.write()

def Hour_and_minute_same(): #A function to run when the hour and minute occupy the same neopixel.
    ring_clear()
    pixel = clock_position(minutehand)
    if minute - (minutehand * 5) == 0:
        ring[pixel] = (30,0,60)
    elif minute - (minutehand * 5) == 1:
        ring[pixel] = (45,0,45)
    elif minute - (minutehand * 5) == 2:
        ring[pixel] = (60,0,60)
    elif minute - (minutehand * 5) == 3:
        ring[pixel] = (60,0,45)
    elif minute - (minutehand * 5) == 4:
        ring[pixel] = (60,0,30)
    ring.write()

def Hour_and_minute_NOT_same(): #A function to run when the hour and minute occupy different neopixels.
    ring_clear()
    hour_pixel = clock_position(hourhand)
    minute_pixel = clock_position(minutehand)
    ring[hour_pixel] = (0,0,60) # Sets the hour hand colour (blue)
    if minute - (minutehand * 5) == 0:
        ring[minute_pixel] = (60,0,0)
    elif minute - (minutehand * 5) == 1:
        ring[minute_pixel] = (60,30,0)
    elif minute - (minutehand * 5) == 2:
        ring[minute_pixel] = (60,60,0)
    elif minute - (minutehand * 5) == 3:
        ring[minute_pixel] = (30,60,0)
    elif minute - (minutehand * 5) == 4:
        ring[minute_pixel] = (0,60,0)
    ring.write()

#Start Up Display:
for i in range(Number_neopixels):
    pixel_index = (Offset + i) % Number_neopixels
    ring[pixel_index] = spectrum[i]
    ring.write()
    time.sleep(1 / Number_neopixels)  # 1 sec / 12 = 0.0833 sec per pixel
steps = 40
for fade in range(steps, -1, -1):
    for j in range(Number_neopixels):
        r, g, b = ring[j]
        ring[j] = (int(r * fade / steps), int(g * fade / steps), int(b * fade / steps))
    ring.write()
    time.sleep(2 / steps)

ring.fill((0,0,0))
ring.write()

while True:
    current_time = rtc.datetime() #Gets real time
    hour_24 = current_time[4] #Gets the hour (in 24 hour format)
    minute = current_time[5] #Gets the minute
    second = current_time[6] #Gets the second

    minutehand = (minute // 5) #Divides by 5 and rounds down to work out which of the 12 numbers around the dial the minute corresponds to e.g. minutes 5-9 correspond to 1, 10-14 correspond to 2

    # Add 1 hour if DST switch is ON (switched on = 0)
    if dst_switch.value() == 0:
        hour_24 = (hour_24 + 1) % 24

    # Work out where the hour hand will be at all 24 hours of the day
    if 0 <= hour_24 < 12:
        hourhand = hour_24  #If hour in 24hr format is 1-11 then it is the same in 12 hour format
    else:
        hourhand = hour_24 - 12 #If hour in 24hr format is 12-24 then minus 12 to get 12 hour format

    #Note that a clock goes 1-12 but the LEDs on the ring are 0-11 so the "12" position is LED position 0
    if (minutehand+1) / (hourhand+1) == 1: #Works out whether the minute and hour take up the same neopixel.  Adding 1 to both numbers avoids dividing by 0 which causes an error
        Hour_and_minute_same() #Runs the function for if the hour and minute DO take up the same neopixel
    else:
        Hour_and_minute_NOT_same() #Runs the function for if the hour and minute don't take up the same neopixel

    if second == 1:
        print_info() #Print info once a minute
    else:
        pass
    time.sleep(1)

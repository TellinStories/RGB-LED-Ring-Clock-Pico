"""
RGB LED Ring Clock: Set Time Utility Script

Copyright (c) 2026 John Dovey

Released under the MIT License.
See LICENSE file in the repository for full licence text.
"""

import machine
from ds3231 import DS3231

i2c = machine.I2C(0, scl=machine.Pin(21), sda=machine.Pin(20))
rtc = DS3231(i2c)

# Set time if needed (year [4 digit], month, day, weekday [Mon = 1, Sun = 7], hour [0-23], minute, second, subsecond [set to 0])
rtc.datetime((2026, 1, 6, 2, 21, 44, 0, 0))

print("RTC time set!")
print(rtc.datetime())

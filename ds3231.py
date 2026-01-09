"""
RGB LED Ring Clock: DS3231 Library
Raspberry Pi Pico + NeoPixel ring + DS3231 RTC

Copyright (c) 2026 John Dovey

Released under the MIT License.
See LICENSE file in the repository for full licence text.
"""


import time

class DS3231:
    def __init__(self, i2c, address=0x68):
        self.i2c = i2c
        self.addr = address

    def _bcd2bin(self, value):
        return (value // 16) * 10 + (value % 16)

    def _bin2bcd(self, value):
        return (value // 10) * 16 + (value % 10)

    def datetime(self, datetime=None):
        if datetime is None:
            # Read from RTC
            data = self.i2c.readfrom_mem(self.addr, 0x00, 7)
            second = self._bcd2bin(data[0])
            minute = self._bcd2bin(data[1])
            hour = self._bcd2bin(data[2])
            weekday = self._bcd2bin(data[3])
            day = self._bcd2bin(data[4])
            month = self._bcd2bin(data[5] & 0x1F)
            year = self._bcd2bin(data[6]) + 2000
            return (year, month, day, weekday, hour, minute, second, 0)
        else:
            # Write to RTC
            year, month, day, weekday, hour, minute, second, _ = datetime
            data = bytearray(7)
            data[0] = self._bin2bcd(second)
            data[1] = self._bin2bcd(minute)
            data[2] = self._bin2bcd(hour)
            data[3] = self._bin2bcd(weekday)
            data[4] = self._bin2bcd(day)
            data[5] = self._bin2bcd(month)
            data[6] = self._bin2bcd(year - 2000)
            self.i2c.writeto_mem(self.addr, 0x00, data)

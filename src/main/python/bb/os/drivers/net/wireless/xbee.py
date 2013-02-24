#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

import sys
import serial
import time

class Serial(serial.Serial):

    def open(self, port, baudrate):
        try:
            self.__serial = pyserial.Serial(port=port, baudrate=baudrate)
        except serial.SerialException, e:
            print >>sys.stderr, "Can not open serial port %s: %s" % (port, e)
            sys.exit(0)

class XBee(object):
    # Carriage Return character
    CR = chr(13)

    def __init__(self):
        self.serial = None

    def open(self, serial):
        self.serial = serial

    def close(self):
        """Close serial driver."""
        self.serial.close()

    def tx(self, array, sz=None):
        if not isinstance(array, bytearray):
            raise Exception("Not a bytearray type")
        self.serial.write(array)

    def tx_str(self, string):
        self.serial.write(string)

    def rx(self, sz):
        return self.serial.read(sz)

    def init_at(self):
        """Configure for low guard time for AT mode. Requires 5 seconds.
        Required if short_at_command() or at_command() used."""
        time.sleep(3)
        self.tx_str("+++")
        time.sleep(2)
        if self.rx(2) != "OK":
            print "Cannot enter into Command Mode"
        self.serial.flushInput()
        self.tx_str("ATGT 3,CN")
        self.tx_str(self.CR) # transmit CR
        time.sleep(0.5)
        if self.rx(2) != "OK":
            print "?"
        self.serial.flushInput()

    def short_at_command(self, command):
        """This method ommits optional parameter that we can define while
        sending AT command. See at_command() for more information."""
        time.sleep(0.1)
        self.tx_str("+++") # enter into Command Mode
        time.sleep(0.1)
        self.serial.flushInput()
        self.tx_str("AT" + command)
        self.tx_str(self.CR)
        self.tx_str("ATCN") # exit from Command Mode
        self.tx_str(self.CR)
        time.sleep(0.01)

    def at_command(self, command, parameter):
        """Send AT commands and parameters by using the following syntax:
        "AT" Prefix + ASCII Command + Space (Optional) + Parameter (Optional, Hex) + CR
        Example: [AT|DL|1F|<CR>]"""
        time.sleep(0.1)
        self.tx_str("+++") # enter into Command Mode
        time.sleep(0.1)
        self.serial.flushInput()
        self.tx_str("AT" + command)
        self.tx_hex(parameter)
        self.tx_str(self.CR)
        self.tx_str("ATCN") # exit from Command Mode
        self.tx_str(self.CR)
        time.sleep(0.01)

    def get_serial_number_high(self):
        """Return high 32 bits of the RF module's unique IEEE 64-bit address."""
        self.short_at_command("SH")
        return self.rx(4)

    def get_serial_number_low(self):
        """Return low 32 bits of the RF module's unique IEEE 64-bit address."""
        self.short_at_command("SL")
        return self.rx(4)

    def get_serial_number(self):
        """Return the RF module's unique IEEE 64-bit address."""
        return "%s%s" % (self.get_serial_number_high(),\
                         self.get_serial_number_low())

    def get_firmware_version(self):
        """Read firmware version of the RF module."""
        self.short_at_command("VR")
        return self.rx(4)

    def get_hardware_version(self):
        """Read hardware version of the RF module."""
        self.short_at_command("HV")
        return self.rx(4)

    def get_received_signal_strength(self):
        """Read signal level [in dB] of last good packet received (RSSI).
        Absolute value is reported. (For example: 0x58 = -88 dBm) Reported value
        is accurate between -40 dBm and RX sensitivity."""
        self.short_at_command("DB")
        return self.rx(2)

    def get_power_level(self):
        self.short_at_command("PL")
        return int(self.rx(1))

    def get_pan_id(self):
        self.short_at_command("ID")
        return self.rx(4)

    def translate_power_level_value(self, value):
        """Provides understanding of power level value."""
        if value == 1:
            return "-10/10 dBm"
        elif value == 4:
            return "0/18 dBm"

if __name__ == '__main__':
    serial = Serial()
    serial.open("/dev/ttyUSB0", 9600)
    driver = XBee()
    driver.open(serial)
    driver.init_at() # initialize AT mode
    print "Test"
    print "PAN (PERSONAL AREA NETWORK) ID", "=", driver.get_pan_id()
    print "RF module's unique EEEI address", "=", driver.get_serial_number()
    print "Modem firmware version", "=", driver.get_firmware_version()
    print "Hardware version", "=", driver.get_hardware_version()
    power_level = driver.get_power_level()
    print "Power level =", power_level,\
        "(%s)" % driver.translate_power_level_value(power_level)
    driver.close()

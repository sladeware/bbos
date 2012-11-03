#!/usr/bin/env python

from bb.hardware.devices import Device
from bb.os.drivers.onewire.slaves import DS18B20Driver

class DS18B20(Device):
  DRIVER_CLASS = DS18B20Driver

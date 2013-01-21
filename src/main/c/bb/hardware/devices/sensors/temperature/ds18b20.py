#!/usr/bin/env python
#
# http://bionicbunny.org/

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

from bb.app.os.drivers.onewire.slaves import DS18B20Driver
from bb.hardware.devices import Device

class DS18B20(Device):

  DRIVER_CLASS = DS18B20Driver

#!/usr/bin/env python
#
# http://bionicbunny.org/
# Copyright (c) 2012 Sladeware LLC
#
# Author: Oleksandr Sviridenko

from bb.app.os.drivers.onewire.slaves import DS18B20Driver
from bb.app.hardware.devices import Device

class DS18B20(Device):

  driver_class = DS18B20Driver

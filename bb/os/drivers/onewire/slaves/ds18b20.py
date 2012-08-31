#!/usr/bin/env python

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'
__author__ = 'Oleksandr Sviridenko'

from bb.os.drivers import Driver

class DS18B20Driver(Driver):
  NAME='DS18B20_DRIVER'
  RUNNER='ds18b20_driver_runner'
  MESSAGE_HANDLERS = {
    'READ_TEMPERATURE': 'ds18b20_read_temperature'
  }

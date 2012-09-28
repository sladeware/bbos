#!/usr/bin/env python

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'
__author__ = 'Oleksandr Sviridenko'

from bb.os import Message, Driver

class DS18B20Driver(Driver):
  NAME='DS18B20_DRIVER'
  RUNNER='ds18b20_driver_runner'
  MESSAGE_HANDLERS = {
    Message('READ_TEMPERATURE', [('dq_pin', 2)], [('value', 2)]): 'ds18b20_read_temperature'
  }

#!/usr/bin/env python

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'
__author__ = 'Oleksandr Sviridenko'

import bb
from bb.os.drivers.gpio.button_driver import ButtonDriver

with ButtonDriver as bundle:
  bundle.build_cases.update({
    'propeller': {
      'srcs': ('button.c',)
      }
    })

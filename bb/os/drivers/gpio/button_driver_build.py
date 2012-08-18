#!/usr/bin/env python

import bb
from bb.os.drivers.gpio.button_driver import ButtonDriver

bb.Builder.rule(ButtonDriver, {
    'PropellerToolchain': {
      'srcs': ('button.c',)
      }
    })

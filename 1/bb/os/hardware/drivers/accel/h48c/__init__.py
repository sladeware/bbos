#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

import random

from bb import os
from bb.os.hardware import Driver

def h48c_open():
    pass
    
def h48c_freefall():
    return int(random.random() + 0.1)

class H48C_GFORCE_AOX(os.Command):
    pass

class H48C_GFORCE_AOY(os.Command):
    pass

class H48C_GFORCE_AOZ(os.Command):
    pass

class H48C_FREEFALL(os.Command):
    """Free fall detection"""

class h48c(Driver):
    name='H48C'
    description='H48C Accelerometer Driver'
    commands=(os.BBOS_DRIVER_OPEN, os.BBOS_DRIVER_CLOSE, H48C_FREEFALL, \
              H48C_GFORCE_AOX, H48C_GFORCE_AOY, H48C_GFORCE_AOZ)

    @Driver.runner
    def h48c_runner(self):
        message = self.get_message()
        if message:
            if message.get_command() is os.BBOS_DRIVER_OPEN:
                h48c_open()
            elif message.get_command() is H48C_FREEFALL:
                message.set_data(h48c_freefall())
            sender = message.get_sender()
            message.set_sender(self.name)
            os.get_running_kernel().send_message(sender, message)

import bb.os.hardware.drivers.accel.h48c.setup


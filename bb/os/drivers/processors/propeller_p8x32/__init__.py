#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

"""Driver for Propeller P8X32 processor."""

from bb.os import get_running_kernel

def on_load():
    get_running_kernel().load_module("bb.os.drivers.gpio.propeller_p8x32_gpio")
    
def on_unload():
    pass


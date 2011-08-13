#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

from bb.builder.project import Wrapper
from bb.os.hardware.drivers.serial.p8x32_uart import P8X32Uart

@Wrapper.bind("on_add", P8X32Uart)
def add_sources(driver, project):
    pass

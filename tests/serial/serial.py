#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

from bb.os.kernel import Kernel
from bb.os.kernel.schedulers import StaticScheduler
import time

kernel = Kernel()
kernel.set_scheduler(StaticScheduler())
#uart = kernel.load_module('bb.os.hardware.drivers.serial.p8x32_uart')
#print uart
uart1 = kernel.load_module('bb.os.hardware.drivers.gpio.p8x32_gpio')
uart2 = kernel.load_module('bb.os.hardware.drivers.gpio.p8x32_gpio')

uart1.NUMBER_GPIOS = 2
print uart1.NUMBER_GPIOS
print uart2.NUMBER_GPIOS

exit()

def demo():
    #settings = uart.Settings(rx=0, tx=1, simulation_port='/dev/ttySL0')
    #uart.uart_open(settings)
    time.sleep(2)

kernel.add_thread("DEMO", demo)

kernel.start()

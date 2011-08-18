#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

from bb.os.kernel import get_running_kernel, get_running_thread, Driver, Message
from bb.os.drivers.gpio.core import gpios_map, gpios_bitmap

def gpio_open(mask):
    global gpios_bitmap
    # Check whether required pins are already opened
    if not mask ^ gpios_bitmap:
        return True
    # Send a message to GPIO driver to open required pins
    get_running_kernel().send_message('P8X32_GPIO', Message('BBOS_DRIVER_OPEN', mask))
    return False

def gpio_direction_output(pin, value):
    """Configure direction as OUTPUT."""
    # Simulation
    gpio = gpios_map[pin]
    gpio.direction = 'OUTPUT'
    gpio.value = value
    get_running_kernel().printer("GPIO#%d direction is %s, value is %s" %\
                                     (pin, gpio.direction, gpio.value))

def gpio_direction_input(pin):
    """Configure direction as INPUT."""
    gpio = gpios_map[pin]
    gpio.direction = 'INPUT'
    get_running_kernel().printer("GPIO#%d direction is %s" % (pin, gpio.direction))

def gpio_set_value(pin, value):
    pass

def gpio_get_value(pin, value):
    pass

class P8X32GPIODriver(Driver):
    name="P8X32_GPIO"
    commands=('BBOS_DRIVER_OPEN', 'BBOS_DRIVER_CLOSE')

    def p8x32_gpio_open(self, mask):
        global gpios_bitmap
        # Look up for the pins that have to be opened
        for pin in range(32):
            if mask & 1:
                if gpios_map[pin].owner:
                    get_running_kernel().printer("Pin %d is already owned by %s" % 
                                                 (pin, gpios_map[pin].owner))
                else:
                    gpios_map[pin].owner = get_running_thread().get_name()
                    get_running_kernel().printer("Open pin %d" % pin)
                    gpios_bitmap |= (1 << pin)
            mask >>= 1

    def p8x32_gpio_close(self, mask):
        pass

    @Driver.runner
    def p8x32_gpio_runner(self):
        message = get_running_kernel().receive_message()
        if message:
            if message.get_command() == 'BBOS_DRIVER_OPEN':
                self.p8x32_gpio_open(message.get_data())
            elif message.get_command() == 'BBOS_DRIVER_CLOSE':
                self.p8x32_gpio_close(message.get_data())

# Register P8X32-GPIO driver
get_running_kernel().register_driver(P8X32GPIODriver())

import bb.os.drivers.gpio.p8x32_gpio_setup

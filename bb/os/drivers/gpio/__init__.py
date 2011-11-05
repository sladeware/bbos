#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

from bb.os import get_running_kernel, get_running_thread, Driver, Device, \
    Messenger

# This values will be taken from the processor's description
PROCESSOR_NUM_GPIOS = 256

class GPIOPin(object):
    """This class describes a single GPIO pin."""
    def __init__(self, direction=None, value=None):
        # The following attributes are for simulation purposes
        self.direction = direction or GPIODriver.GPIO_DIRECTION_INPUT
        self.value = value or GPIODriver.GPIO_INIT_LOW

class GPIO(object):
    def __init__(self, owner=None):
        self.owner = owner

class GPIOMessenger(Messenger):
    PORT_NAME_FORMAT = "GPIO_MESSENGER_PORT_%d"

    def __init__(self, *args, **kargs):
        Messenger.__init__(self, *args, **kargs)
        # Initialize map of GPIOs. Each GPIO pin is represented by GPIO class.
        # The size of map equals to number of GPIOs.
        self.gpios_map = [None] * PROCESSOR_NUM_GPIOS
        for gpio in range(PROCESSOR_NUM_GPIOS):
            self.gpios_map[gpio] = GPIO()

    @Messenger.message_handler("GPIO_OPEN")
    def gpio_open_handler(self, message):
        mask = message.get_data()
        # Look up for the pins that have to be opened
        for pin in range(32):
            if mask & 1:
                if self.gpios_map[pin].owner:
                    get_running_kernel().echo("Pin %d is already owned by %s"
                                              % (pin, self.gpios_map[pin].owner))
                else:
                    self.gpios_map[pin].owner = get_running_thread().get_name()
                    get_running_kernel().echo("Open pin %d" % pin)
            mask >>= 1
        # Reuse received message to send respose
        get_running_kernel().send_message(message.get_sender(), message)

    @Messenger.message_handler("GPIO_CLOSE")
    def gpio_close_handler(self, mask):
        pass

class GPIODriver(Driver):
    MESSENGER_CLASS = GPIOMessenger

    GPIO_DIRECTION_INPUT=0
    GPIO_DIRECTION_OUPUT=1
    GPIO_INIT_LOW=0
    GPIO_INIT_HIGH=1

    def __init__(self):
        Driver.__init__(self)
        # Initialize map of GPIOs. Each GPIO pin is represented by GPIO class.
        # The size of map equals to number of GPIOs.
        self.gpios_map = [None] * PROCESSOR_NUM_GPIOS
        for gpio in range(PROCESSOR_NUM_GPIOS):
            self.gpios_map[gpio] = GPIOPin()
        # Bitmap
        self.gpios_bitmap = 0

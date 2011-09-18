#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

# This values will be taken from the processor's description
PROCESSOR_NUM_GPIOS = 256

GPIO_DIRECTION_INPUT = 0
GPIO_DIRECTION_OUPUT = 1
GPIO_INIT_LOW = 0
GPIO_INIT_HIGH = 1

class GPIODescription(object):
    """This class describes a single GPIO pin."""
    def __init__(self, owner=None,
                 direction=GPIO_DIRECTION_INPUT,
                 value=GPIO_INIT_LOW):
        self.owner = owner
        # The following attributes are for simulation purposes
        self.direction = direction
        self.value = value

# Initialize map of GPIOs. Each GPIO pin is represented by GPIO class. The
# size of map equals to number of GPIOs.
gpios_map = [None] * PROCESSOR_NUM_GPIOS
for gpio in range(PROCESSOR_NUM_GPIOS):
    gpios_map[gpio] = GPIODescription()
# Bitmap
gpios_bitmap = 0

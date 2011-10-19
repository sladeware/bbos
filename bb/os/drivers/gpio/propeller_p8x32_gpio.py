#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

from bb.os import get_running_kernel, get_running_thread, Driver, Message, \
    Port, Messenger
from bb.os.drivers.gpio import GPIODriver, GPIODevice, GPIOManager

class PropellerP8X32GPIODevice(GPIODevice):
    name="PROPELLER_P8X32_GPIO_DEVICE"

class PropellerP8X32GPIODriver(GPIODriver):
    name="PROPELLER_P8X32_GPIO_DRIVER"
    version="0.0.0"
    port_name="PROPELLER_P8X32_GPIO_DRIVER_PORT"

    def init(self):
        get_running_kernel().add_port(Port(self.port_name, 2))
        manager = GPIOManager(self.name, port_name=self.port_name)

    def open(self, mask):
        """Send BBOS_DRIVER_OPEN message."""
        message = get_running_kernel().receive_message()
        if message:
            if message.get_command() == "GPIO_OPEN" and message.get_data() & mask:
                get_running_kernel().free_message(message)
                return True
            return False # ?!
        # Send a message to GPIO driver to open required pins
        message = get_running_kernel().alloc_message("GPIO_OPEN", mask)
        if not message:
            printk("P8X32 GPIO can not allocate message")
            return
        get_running_kernel().send_message(self.port_name, message)
        return False

    def close(self, mask):
        pass

    def direction_output(self, pin, value):
        """Configure direction as OUTPUT."""
        # Simulation
        gpio = self.gpios_map[pin]
        gpio.direction = 'OUTPUT'
        gpio.value = value
        get_running_kernel().echo("GPIO#%d direction is %s, value is %s"
            % (pin, gpio.direction, gpio.value))

    def direction_input(pin):
        """Configure direction as INPUT."""
        gpio = self.gpios_map[pin]
        gpio.direction = 'INPUT'
        get_running_kernel().echo("GPIO#%d direction is %s"
            % (pin, gpio.direction))

    def set_value(pin, value):
        pass

    def get_value(pin, value):
        pass

def on_load():
    driver = get_running_kernel().register_driver(PropellerP8X32GPIODriver)
    propeller_p8x32_gpio = PropellerP8X32GPIODevice(driver=driver)
    get_running_kernel().register_device(propeller_p8x32_gpio)

def on_unload():
    get_running_kernel().unregister_driver(PropellerP8X32GPIODriver)



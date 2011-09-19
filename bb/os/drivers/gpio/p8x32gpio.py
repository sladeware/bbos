__copyright__ = "Copyright (c) 2011 Sladeware LLC"

from bb.os.kernel import get_running_kernel, get_running_thread, Driver, Message, printk
from bb.os.drivers.gpio.core import gpios_map, gpios_bitmap

waiting = 0

def open(mask):
    """Send BBOS_DRIVER_OPEN message to gpio driver."""
    global waiting
    if mask & waiting:
        message = get_running_kernel().receive_message("P8X32_GPIO_INTERFACE_PORT")
        if not message:
            return False
        if message.get_command() == "GPIO_OPEN" and message.get_data() & mask:
            get_running_kernel().free_message(message)
            return True
    # Send a message to GPIO driver to open required pins
    message = get_running_kernel().alloc_message("P8X32_GPIO_INTERFACE_PORT",
                                                 "GPIO_OPEN", mask)
    if not message:
        printk("P8X32 GPIO can not allocate message")
        return
    get_running_kernel().send_message("P8X32_GPIO_DRIVER_PORT", message)
    waiting ^= mask
    return False

def close(mask):
    pass

def direction_output(pin, value):
    """Configure direction as OUTPUT."""
    # Simulation
    gpio = gpios_map[pin]
    gpio.direction = 'OUTPUT'
    gpio.value = value
    printk("GPIO#%d direction is %s, value is %s" % \
               (pin, gpio.direction, gpio.value))

def direction_input(pin):
    """Configure direction as INPUT."""
    gpio = gpios_map[pin]
    gpio.direction = 'INPUT'
    printk("GPIO#%d direction is %s" % (pin, gpio.direction))

def set_value(pin, value):
    pass

def get_value(pin, value):
    pass

class P8X32GPIODriver(Driver):
    name='P8X32_GPIO_DRIVER'
    commands=('GPIO_OPEN', 'GPIO_CLOSE')

    def p8x32_gpio_open(self, message):
        global gpios_bitmap
        mask = message.get_data()
        # Look up for the pins that have to be opened
        for pin in range(32):
            if mask & 1:
                if gpios_map[pin].owner:
                    printk("Pin %d is already owned by %s"
                           % (pin, gpios_map[pin].owner))
                else:
                    gpios_map[pin].owner = get_running_thread().get_name()
                    printk("Open pin %d" % pin)
                    gpios_bitmap |= (1 << pin)
            mask >>= 1
        # Reuse received message to send respose
        get_running_kernel().send_message(message.get_sender(), message)

    def p8x32_gpio_close(self, mask):
        pass

    @Driver.runner
    def p8x32_gpio_runner(self):
        message = get_running_kernel().receive_message("P8X32_GPIO_DRIVER_PORT")
        if not message: return
        if message.get_command() == 'GPIO_OPEN':
            self.p8x32_gpio_open(message)
        elif message.get_command() == 'GPIO_CLOSE':
            self.p8x32_gpio_close(message.get_data())

def bootstrap(args):
    get_running_kernel().add_port("P8X32_GPIO_INTERFACE_PORT", 2)
    get_running_kernel().add_port("P8X32_GPIO_DRIVER_PORT", 2)
    # Register P8X32-GPIO driver
    driver = P8X32GPIODriver()
    get_running_kernel().register_driver(driver)

import bb.os.drivers.gpio.p8x32_gpio_setup


__copyright__ = "Copyright (c) 2011 Sladeware LLC"

from bb.os.kernel import get_running_kernel, get_running_thread, Driver, Message

# This values will be taken from the processor's description
NUMBER_GPIOS = 256

GPIO_DIRECTION_INPUT = 0
GPIO_DIRECTION_OUPUT = 1
GPIO_INIT_LOW = 0
GPIO_INIT_HIGH = 1

class GPIO(object):
    """This class describes a single GPIO pin."""
    def __init__(self, owner=None, 
                 direction=GPIO_DIRECTION_INPUT, 
                 value=GPIO_INIT_LOW):
        self.owner = owner
        self.direction = direction
        self.value = value

# Initialize map of GPIOs. Each GPIO pin is represented by GPIO class. The
# size of map equals to number of GPIOs.
gpios_map = [None] * NUMBER_GPIOS
for gpio in range(NUMBER_GPIOS):
    gpios_map[gpio] = GPIO()
# Bitmap
gpios_bitmap = 0

def gpio_open(mask):
    global gpios_bitmap
    # Check whether required pins are already opened
    if not mask ^ gpios_bitmap:
        return True
    # Send a message to GPIO driver to open required pins
    get_running_kernel().send_message('P8X32_GPIO', Message('BBOS_DRIVER_OPEN', mask))
    return False

def gpio_set_direction(pin, direction):
    gpio = gpios_map[pin]
    gpio.direction = direction
    get_running_kernel().printer("Pin %d direction is %d" % (pin, direction))

def gpio_get_direction(pin):
    pass

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

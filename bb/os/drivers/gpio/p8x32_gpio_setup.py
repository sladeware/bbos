
__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

from bb.builder.project import Wrapper

from bb.os.hardware.drivers.gpio.p8x32_gpio import P8X32GPIODriver

@Wrapper.bind("on_add", P8X32GPIODriver)
def add_p8x32_gpio_driver(driver, project):
    pass

from bbos_application import *
from bbos_board import *
from bbos_compiler import *
from bbos_driver import *
from bbos_process import *
from propeller_demo_board import *

gpio_driver = BBOSDriver(boot="gpio_driver_init",
                         main="gpio_driver",
                         exit="gpio_driver_exit",
                         files=["/hardware/driver/gpio.c",
                                "/hardware/driver/propeller.c"],
                         name="gpio",
                         port="GPIO_DRIVER_PORT",
                         version=2)

finger = BBOSProcess(compiler=BBOSCompiler(),
                     drivers=[gpio_driver],                         
                     files=["finger.c"],
                     ipc=True,
                     mempools=["MOVE_MESSAGES"],
                     ports=["MOVE_PORT"],
                     threads=["move"])

PropellerDemoBoard(finger, 12)

application = BBOSApplication(processes=[finger])


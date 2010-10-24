from bbos_application import *
from bbos_board import *
from bbos_compiler import *
from bbos_driver import *
from bbos_process import *
from propeller_demo_board import *

gpio_driver = BBOSDriver(
    name="gpio",
    version=2,
    ports=["GPIO_DRIVER_PORT"],
    handlers=["gpio_driver_init","gpio_driver_main","gpio_driver_exit"],
    files=["/hardware/driver/gpio.c", "/hardware/driver/propeller.c"],
    )

finger = BBOSProcess(
    compiler=BBOSCompiler(),
    drivers=[gpio_driver],                         
    files=["finger.c"],
    ipc=True,
    mempools=[],
    ports=["FINGER_PORT"],
    static_scheduler=True,
    threads=["move"]
)

board = PropellerDemoBoard(
    process=finger,
    config={
        'memsize': 32
        }
    )
    

application = BBOSApplication(
    name="RobotHand",
    devices=[board]
    )


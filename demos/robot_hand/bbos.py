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
    boot="gpio_driver_init",
    main="gpio_driver_main",
    exit="gpio_driver_exit",
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
    processes=[finger],
    memsize=32
    )
    

application = BBOSApplication(
    name="RobotHand",
    boards=[board]
    )


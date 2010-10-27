"""An example bbos.py file defining the late binding of the robot hand.
"""

from lib.bbos_application import *
from lib.bbos_board import *
from lib.bbos_compiler import *
from lib.bbos_driver import *
from lib.bbos_process import *
from lib.bbos_static_scheduler import *
from boards.propeller_demo_board import *

gpio_driver = BBOSDriver(
    name="gpio",
    version=2,
    ports=["GPIO_DRIVER_PORT"],
    files=["/hardware/driver/gpio.c", "/hardware/driver/propeller.c"],
    )

finger = BBOSProcess(
    compiler=BBOSCompiler(),
    drivers=[gpio_driver],                         
    files=["finger.c"],
    ipc=True,
    mempools=[],
    ports=["FINGER_PORT"],
    static_scheduler=StaticScheduler(["move", "gpio_driver_main"]),
    threads=["move"]
)

board = PropellerDemoBoard(
    processes=[finger],
    memsize=32
    )
    
# The application varible of type BBOSApplication(...) must be defined
application = BBOSApplication(
    name="RobotHand",
    boards=[board]
    )


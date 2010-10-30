"""An example bbos.py file defining the late binding of the robot hand.
"""

from bbos.application import *
from bbos.compiler import *
from bbos.hardware.board import *
from bbos.hardware.boards.propeller_demo_board import *
from bbos.hardware.driver import *
from bbos.kernel.bbos_process import *
from bbos.kernel.process.scheduler.static import *

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
    name="finger",
    ports=["FINGER_PORT"],
    static_scheduler=StaticScheduler(["move", "gpio_driver_main"]),
    threads=["move"]
)

propeller_demo_board = PropellerDemoBoard(
    processes=[finger],
    memsize=32
    )
    
# The application varible of type BBOSApplication(...) must be defined
application = BBOSApplication(
    name="RobotHand",
    boards=[propeller_demo_board]
    )


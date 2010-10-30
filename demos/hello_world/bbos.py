"""An example bbos.py file for the quad core X86 simulation of hello world.
"""

from bbos.application import *
from bbos.compiler import *
from bbos.hardware.board import *
from bbos.hardware.boards.propeller_demo_board import *
from bbos.hardware.boards.quad_x86_simulation_board import *
from bbos.kernel.bbos_process import *

hello_world = BBOSProcess(
    compiler=BBOSCompiler(),
    drivers=[],
    files=["hello_world.c"],
    ipc=None,
    mempools=[],
    name="demo",
    ports=[],
    static_scheduler=None,
    threads=["hello_world"]
)

quad_core_x86_simulation_board = QuadX86SimulationBoard(
    processes=[hello_world]
    )
    
hello_world_cog = BBOSProcess(
    compiler=BBOSCompiler(),
    drivers=[],
    files=["hello_world.c"],
    ipc=None,
    mempools=[],
    name="demo_cog",
    ports=[],
    static_scheduler=None,
    threads=["hello_world"]
)

propeller_demo_board = PropellerDemoBoard(
    processes=[hello_world_cog],
    memsize=2
    )
    
# The application varible of type BBOSApplication(...) must be defined
application = BBOSApplication(
    name="HelloWorld",
    boards=[quad_core_x86_simulation_board, propeller_demo_board]
    )


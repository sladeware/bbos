"""An example bbos.py file for the quad core X86 simulation of hello world.
"""

__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

import sys
import os

from bbos.project import Project
from bbos.kernel import Kernel
from bbos.kernel.schedulers import FCFS
from bbos.hardware.boards import QuadX86SimulationBoard

def main():
    # Start build meta operating system
    demo = Kernel()
    # Scheduling
    demo.set_scheduler( FCFS() )
    # Threads
    demo.add_thread("DEMO")
    # Create and configure project
    proj = Project(board=QuadX86SimulationBoard([demo]))
    # Configure
    proj.config()

if __name__ == '__main__':
    sys.exit(main())




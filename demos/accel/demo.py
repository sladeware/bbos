
__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

import sys
import os

from bbos.project import Project
from bbos.kernel import Kernel
from bbos.kernel.schedulers import FCFS
from bbos.hardware.boards import PropellerDemoBoard

def main():
    # Start to build meta operating system
    demo = Kernel()
    # First-Come-First-Served scheduling policy
    demo.set_scheduler( FCFS() )
    # Add application threads
    demo.add_thread("DEMO")
    # Load modules
    demo.add_module("bbos.hardware.drivers.accel.h48c")
    proj = Project(board=PropellerDemoBoard([demo]))
    # Configure project
    proj.config()

if __name__ == '__main__':
    sys.exit(main())





__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

import sys
import os

from bbos.project import Project
from bbos.kernel import Kernel
from bbos.kernel.thread import Thread
from bbos.kernel.schedulers import FCFS, StateMachine
from bbos.kernel.scheduler import StaticScheduler
from bbos.hardware.boards import PropellerDemoBoard

def main():
    # Start to build meta operating system
    demo = Kernel()
    # Add application threads
    freefall = demo.add_thread(Thread("FREEFALL", "freefall"))
    # Load modules
    h48c = demo.add_module("bbos.hardware.drivers.accel.h48c")
    # Select scheduling policy
    demo.set_scheduler( FCFS() )
    #demo.set_scheduler( StaticScheduler(order=[freefall, h48c.get_thread()]) )
    # Create the project
    proj = Project(board=PropellerDemoBoard([demo]))
    # Configure project
    proj.config()
    return 0
# main()

if __name__ == '__main__':
    sys.exit(main())




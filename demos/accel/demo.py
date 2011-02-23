
__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

import sys
import os

from bbos.project import Project
from bbos.kernel import Kernel
from bbos.kernel.schedulers import FCFS
from bbos.hardware.boards import PropellerDemoBoard

def main():
    demo = Kernel()
    # First-Come-First-Served scheduling policy
    sched = FCFS()
    demo.set_scheduler(sched)
    demo.add_thread("DEMO")
    demo.add_module("bbos.hardware.drivers.accel.h48c")
    board = PropellerDemoBoard([demo])
    proj = Project(board)
    proj.config()

if __name__ == '__main__':
    sys.exit(main())




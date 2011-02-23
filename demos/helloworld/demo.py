
__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

import sys
import os

from bbos.project import Project
from bbos.kernel import Kernel
from bbos.kernel.schedulers import FCFS
from bbos.hardware.boards import QuadX86SimulationBoard

def main():
    demo = Kernel()
    sched = FCFS()
    demo.set_scheduler(sched)
    demo.add_thread("DEMO")
    simulator = QuadX86SimulationBoard([demo])
    proj = Project(simulator)
    proj.config()

if __name__ == '__main__':
    sys.exit(main())





__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

import sys
import os

from bbos.application import Application
from bbos.kernel import Kernel
from bbos.kernel.thread import Thread
from bbos.kernel.schedulers import FCFS
from bbos.kernel.scheduler import StaticScheduler
from bbos.hardware.boards import PropellerDemoBoard
from builder.projects import CatalinaProject

def main():
    demo = Kernel()
    freefall = demo.add_thread(Thread("FREEFALL", "freefall"))
    h48c = demo.add_module("bbos.hardware.drivers.accel.h48c")
    # Select scheduling policy
    #demo.set_scheduler( FCFS() )
    demo.set_scheduler( StaticScheduler(order=[freefall, h48c.get_thread()]) )
    app = Application(board=PropellerDemoBoard([demo]))
    project = CatalinaProject("demo", verbose=True)
    project.compiler.add_library('ci')
    try:
        project.build([app, os.path.join(os.path.dirname(__file__), "demo.c")], 
                      output_dir=os.path.abspath(os.path.dirname(__file__)),
                      include_dirs=[os.path.abspath(os.path.dirname(__file__))])
    except:
        pass
    return 0

if __name__ == '__main__':
    sys.exit(main())




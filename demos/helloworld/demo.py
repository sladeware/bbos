"""An example bbos.py file for the quad core X86 simulation of hello world.
"""

__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

import sys
import os

from bbos.application import Application
from bbos.kernel import Kernel
from bbos.kernel.thread import Thread
from bbos.kernel.schedulers import FCFS
from bbos.kernel.scheduler import StaticScheduler
from bbos.hardware.boards import QuadX86SimulationBoard
from builder.projects import CProject

def main():
    # Start build meta operating system
    demo = Kernel()
    # Threads
    helloworld = demo.add_thread(Thread("HELLOWORLD", "helloworld"))
    # Scheduling policy
    demo.set_scheduler(StaticScheduler("My own schedule!", order=[helloworld]))
    # Create and configure application
    app = Application(board=QuadX86SimulationBoard([demo]))
    # Configure
    project = CProject("demo", verbose=True)
    project.build([app, os.path.join(os.path.dirname(__file__), "demo.c")], 
                  output_dir=os.path.abspath(os.path.dirname(__file__)),
                  include_dirs=[os.path.abspath(os.path.dirname(__file__))])
    #proj.config()

if __name__ == '__main__':
    sys.exit(main())




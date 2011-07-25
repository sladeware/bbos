
__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

import sys
import os

from bbos.application import Application
from bbos.kernel import Kernel
from bbos.kernel.thread import Thread
from bbos.kernel.scheduler import StaticScheduler
from bbos.hardware.board import Board
from bbos.hardware.processors import PropellerP8X32A
from builder.projects import CatalinaProject
from builder.loaders import BSTLLoader

def main():
    demo = Kernel()
    blink = demo.add_thread(Thread("BLINK", "blink"))
    demo.set_scheduler(StaticScheduler("My own schedule!", order=[blink]))
    app = Application(board=Board("My board", [PropellerP8X32A([demo])]))

    project = CatalinaProject("demo", verbose=True)
    project.set_loader(BSTLLoader())
    project.compiler.add_library('ci')

    try:
        project.build([app, os.path.join(os.path.dirname(__file__), "demo.c")], 
                      output_dir=os.path.abspath(os.path.dirname(__file__)),
                      include_dirs=[os.path.abspath(os.path.dirname(__file__))])
    except:
        pass

    project.load()

    return 0

if __name__ == '__main__':
    sys.exit(main())




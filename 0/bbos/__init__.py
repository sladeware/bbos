
__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

import os

from bbos.component import Component
from bbos.hardware import Hardware
from bbos.kernel import Kernel

class BBOS(Component):
    def __init__(self, name):
        Component.__init__(self, name)
        self.hardware = Hardware()
        self.kernel = Kernel()

    def on_build(self, project):
        project.env['bbos.h'] = os.path.join(project.compiler.get_output_dir(), "bbos.h")
        project.compiler.add_include_dirs([os.environ['BBOSHOME'], project.compiler.get_output_dir()])
        try:
            f = open(project.env['bbos.h'], "w")
        except IOError:
            print "There were problems writing to %s" % "bbos.h"
            traceback.print_exc(file=sys.stderr)
            raise
        f.close()

        project.add_sources([self.hardware, self.kernel])

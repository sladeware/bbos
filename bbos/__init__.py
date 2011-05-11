
__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

from bbos.component import Component
from bbos.hardware import Hardware
from bbos.kernel import Kernel

class BBOS(Component):
    def __init__(self, name):
        Component.__init__(self, name)
        self.hardware = Hardware()
        self.kernel = Kernel()

    def on_build(self, project):
        pass

    def on_add(self, project):
        project.add_source(self.kernel)

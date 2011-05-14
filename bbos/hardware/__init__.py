

__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

from bbos.component import Component

class Hardware(Component):
    def __init__(self):
        Component.__init__(self)
        self.board = None
        self.processor = None
        self.core = None

    def on_build(self, project):
        print "Configuring hardware"
        project.add_source(self.board)
        project.add_source(self.processor)
        project.add_source(self.core)

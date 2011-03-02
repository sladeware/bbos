
__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

from bbos.project import Project

class Component:
    """
    OS component class.
    """
    def __init__(self, name=None):
        self.name = name

    def get_name(self):
        return self.name

    def config(self, proj):
        if not isinstance(proj, Project):
            print "The project instance should based on Project"
            return
        if hasattr(self, '_config'):
            self._config(proj)

    def _config(self, proj):
        pass



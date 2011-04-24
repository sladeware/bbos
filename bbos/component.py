
__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

from builder.project import Extension
from bbos.application import Application

class Component(Extension):
    """
    OS component class.
    """
    def __init__(self, name=None):
        Extension.__init__(self, name)

    def config(self, app):
        if not isinstance(app, Application):
            raise "The application instance should based on Application"
        if hasattr(self, '_config'):
            self._config(app)

    def _config(self, app):
        pass



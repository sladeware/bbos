#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

# The following code has to located right before import's. I think this is
# temporary solution (or maybe not).
class OSObject(object):
    """The root main class for BBOS kernel."""
    pass

class OSObjectMetadata(object):
    NAME = None

    def __init__(self, name=None):
        self.__name = None
        if name:
            self.set_name(name)
        elif hasattr(self, "NAME"):
            self.set_name(self.NAME)

    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

from bb.os.kernel import *
from bb.os.hardware import *

class OS(object):
    """This class describes BB operating system. The Mapping uses this class to
    create OS instance. Once system is created, the mapping will call main entry
    point."""
    def __init__(self, **kargs):
        self.kernel = kernel.Kernel()

    def main(self):
        pass

    def start(self):
        """This method implements OS's activity. You may override this method in
        subclass."""
        self.kernel.start()

#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

from bb.app import Context

# XXX: The following code has to be located right before import's. I think this
# is temporary solution (or maybe not), until we will move this to the separata
# file.
class OSObject(Context):
    """The root main class for BBOS kernel."""
    def __init__(self):
        Context.__init__(self)

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

class OS(object):
    """This class describes BB operating system. The Mapping uses this class to
    create OS instance. Once system is created, the mapping will call main entry
    point and then start() to run the system."""
    def __init__(self, **kargs):
        self.kernel = Kernel()

    def main(self):
        pass

    def start(self):
        """This method implements OS's activity. You may override this method in
        subclass."""
        self.kernel.start()

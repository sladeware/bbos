#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

# The following code has to located right before import's. I think this is
# temporary solution (or maybe not).
class OSObject(object):
    pass

class OSObjectMetadata(object):
    name=None

    def __init__(self, name=None):
        self.__name = None
        if name:
            self.set_name(name)
        elif hasattr(self, "name"):
            self.set_name(getattr(self, "name"))

    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

from bb.os.kernel import *
from bb.os.hardware import *

class OS(object):
    def __init__(self):
        self.kernel = kernel.Kernel()

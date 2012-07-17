#!/usr/bin/env python

from bb.os.microkernel import Microkernel
from bb.build import packager
from bb.build import builder

class OS(object):
    def __init__(self, threads=[]):
        self._microkernel = Microkernel()
        if threads:
            self._microkernel.register_threads(threads)

    def get_microkernel(self):
        return self._microkernel

@builder.dependency_injector(OS)
def _(os):
    dependencies = list()
    microkernel = os.get_microkernel()
    dependencies.append(microkernel)
    dependencies.extend(microkernel.get_threads())
    return dependencies

@packager.pack(OS, "simulator")
class _(packager.Package):
    FILES = ("./../runtime/os/os.py", )

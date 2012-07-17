#!/usr/bin/env python

from bb.runtime.os.microkernel import Microkernel

class OS(object):
    def __init__(self, os):
        self._microkernel = Microkernel(os.get_microkernel())

    def get_microkernel(self):
        return self._microkernel

    @property
    def microkernel(self):
        return self.get_microkernel()

    def main(self):
        self._microkernel.start()

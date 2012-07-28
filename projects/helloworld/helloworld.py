#!/usr/bin/env python

from bb.runtime import Thread
from bb.runtime import os as bbos

class Printer(Thread):
    pass

class OS(bbos.OS):
    def main(self):
        self.microkernel.echo("Hello world!")
        self.microkernel.start()

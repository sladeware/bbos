#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

"""The workstation connects to database and process the packages received from
a network of minimeter devices."""

from bb.app import Mapping
from bb.hardware import Board, Processor, Core
from bb.os import OS, Thread

class WorkstationOS(OS):
    def __init__(self):
        OS.__init__(self)

    def initializer(self):
        """The purpose of this runner is to initialize the workstation: open
        XBEE wireless module."""
        pass

    def main(self):
        self.kernel.add_thread(Thread("INITIALIZER", self.initializer))

class WorkstationBoard(Board):
    """This class describes a board that will be used by workstation. On this
    moment we will use a random board."""
    def __init__(self, mapping):
        # I think, that workstation should include only one single mapping
        if not isinstance(mapping, Mapping):
            raise TypeError("mapping should be a Mapping() instance")
        # Build a random board for the first time
        processor = Processor("A process", 1, [Core("A core", mapping)])
        Board.__init__(self, "A board", 1, [processor])

class Workstation(Mapping):
    os_class = WorkstationOS

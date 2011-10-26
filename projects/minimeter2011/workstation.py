#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

"""The workstation connects to database and process the packages received from
a network of minimeter devices."""

from bb.app import Mapping
from bb.hardware import Board, Processor, Core
from bb.os import OS, Thread
from bb.utils.module import get_file

import sys
try:
    from sqlite3 import *
except ImportError, e:
    print >>sys.stderr, "To continue using workstation, please install sqlite3:"
    print >>sys.stderr, e
    sys.exit(1)

class WorkstationOS(OS):
    def __init__(self, db_name=get_file('workstation.db')):
        OS.__init__(self)
        self.connect = None
        self.cursor = None
        self.init = False

        # The file name of the database
        self.db_name = db_name

    def initializer(self):
        """The purpose of this runner is to initialize the workstation: open
        XBEE wireless module and open the database."""
        if not self.init:
            self.init = True

            # Open the XBEE Wireless Module
            print 'opening the xbee wireless module'
            # UNIMPLEMENTED

            # Open the database
            print 'opening the database'
            self.connect = connect(self.db_name)
            if self.connect:
                self.cursor = self.connect.cursor()
                if self.cursor:
                    print 'database opened successfully'
                else:
                    print 'WARNING: problems getting the database cursor'
            else:
                print 'WARNING: problems opening the database'

    def main(self):
        self.kernel.add_thread(Thread("INITIALIZER", self.initializer))

class WorkstationDevice(Board):
    """This class describes device that will run workstation. On this moment we
    will use a random board."""
    def __init__(self, mapping):
        # I think, that workstation should include only one single mapping
        if not isinstance(mapping, Mapping):
            raise TypeError("mapping should be a Mapping() instance")
        # Build a random board for the first time
        processor = Processor("A process", 1, [Core("A core", mapping)])
        Board.__init__(self, "A board", 1, [processor])

class Workstation(Mapping):
    os_class = WorkstationOS

    def __init__(self, name):
        Mapping.__init__(self, name)
        WorkstationDevice(self)

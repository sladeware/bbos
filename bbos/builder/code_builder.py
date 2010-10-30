"""This class builds the BBOS application code, producing process binaries.
"""

__copyright__ = "Copyright (c) 2010 Slade Maurer, Alexander Sviridenko"

from common import *
import os
import sys

KERNEL_FILES = ["bbos/kernel/time",
                "bbos/kernel/process/port",
                "bbos/kernel/process",
                "bbos/kernel/system",
                "bbos/kernel/mm/mempool",
                "bbos/kernel/process/scheduler/fcfs",
                "bbos/kernel/process/scheduler/static",
                "bbos/kernel/process/thread",
                "bbos/kernel/process/thread/idle",
                "bbos/kernel/hardware",
                "bbos/kernel/application"]

BASE = os.path.abspath(os.path.dirname(sys.argv[0])) + "/../"


class BuildCode:
    def __init__(self, directory, process):
        # The process we're genearting code for
        self.process = process

        # The base directory of the application we are building
        self.application_directory = directory + "/"

        # The files we're going to build for this process
        self.files = [self.application_directory + f[0:-2] for f in self.process.files] + [BASE + f for f in KERNEL_FILES]

    def build(self):
        print "Building code..."
        c = self.process.compiler
        c.includes.append(self.application_directory)
        self._build_objects()
        self._build_process_binary()

    def _build_objects(self):
        c = self.process.compiler
        for f in self.files:
            oc_files = "-c -o " + f + ".o " + f + ".c"
            cmd = c.name + " " + c.options + " " + c.get_includes() + " " + oc_files
            os.system(cmd)

    def _build_process_binary(self):
        c = self.process.compiler
        cmd = c.name + " " + c.options + " -o " + self.application_directory + self.process.name + " "
        for f in self.files:
            cmd += f + ".o "
        os.system(cmd)

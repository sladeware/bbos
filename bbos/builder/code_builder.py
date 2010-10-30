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
                "bbos/kernel/process/thread",
                "bbos/kernel/process/thread/idle",
                "bbos/kernel/hardware",
                "bbos/kernel/application"]

BASE = os.path.abspath(os.path.dirname(sys.argv[0])) + "/../"


class BuildCode:
    def __init__(self, directory, process, test=False):
        # The process we're genearting code for
        self.process = process

        # The base directory of the application we are building
        self.application_directory = directory + "/"

        # The files we're going to build for this process
        self.files = [self.application_directory + f[0:-2] for f in self.process.files] + [BASE + f for f in KERNEL_FILES]
        if self.process.static_scheduler:
            self.files.append("bbos/kernel/process/scheduler/static")
        else:
            self.files.append("bbos/kernel/process/scheduler/fcfs")

        self.test = test

    def build(self):
        lines = []
        print "  Building code..."
        c = self.process.compiler
        c.includes.append(self.application_directory)
        lines += self._build_objects()
        lines.append(self._build_process_binary())
        if self.test:
            return lines

    def _build_objects(self):
        results = []
        c = self.process.compiler
        for f in self.files:
            oc_files = "-c -o " + f + ".o " + f + ".c"
            cmd = c.name + " " + c.options + " " + c.get_includes() + " " + oc_files
            if self.test:
                results.append(cmd)
            else:
                os.system(cmd)
        return results

    def _build_process_binary(self):
        c = self.process.compiler
        cmd = c.name + " " + c.options + " -o " + self.application_directory + self.process.name + " "
        for f in self.files:
            cmd += f + ".o "
        if self.test:
            return cmd
        else:
            os.system(cmd)

"""Base class used to represent a core within a processor.

A Core is the smallest computational unit supported by BBOS. There is one
core per processes and one process per core.
"""

__copyright__ = "Copyright (c) 2010 Slade Maurer, Alexander Sviridenko"

from bbos.kernel.bbos_process import *
from bbos.builder.common import *


class BBOSCore:
    def __init__(self, process):
        # The process running on this core
        assert isinstance(process, BBOSProcess), "process is not a BBOSProcess: %s" % process
        self.process = process

    def modify_compiler_defines(self, defines):
        if self.process.compiler.defines:
            print "WARNING: Not overwriting preexisting compiler defines"
        else:
            self.process.compiler.defines = verify_list(defines)

    def modify_compiler_include_directories(self, dirs):
        if self.process.compiler.includes:
            print "WARNING: Not overwriting preexisting compiler include directories"
        else:
            self.process.compiler.includes = verify_list(dirs)

    def modify_compiler_include_argument(self, arg):
        if self.process.compiler.include_argument:
            print "WARNING: Not overwriting preexisting compiler include argument"
        else:
            self.process.compiler.include_argument = verify_string(arg)

    def modify_compiler_name(self, name):
        if self.process.compiler.name:
            print "WARNING: Not overwriting preexisting compiler name"
        else:
            self.process.compiler.name = verify_string(name)

    def modify_compiler_options(self, options):
        if self.process.compiler.options:
            print "WARNING: Not overwriting preexisting compiler options"
        else:
            self.process.compiler.options = verify_string(options)


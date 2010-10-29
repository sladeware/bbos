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
            print "WARNING: Overwriting preexisting compiler defines"
        self.process.compiler.defines = verify_list(defines)

    def modify_compiler_include_directories(self, dirs):
        if self.process.compiler.includes:
            print "WARNING: Overwriting preexisting compiler include directories"
        self.process.compiler.includes = verify_list(dirs)

    def modify_compiler_include_argument(self, arg):
        if self.process.compiler.include_argument:
            print "WARNING: Overwriting preexisting compiler include argument"
        self.process.compiler.include_argument = verify_string(arg)

    def modify_compiler_name(self, name):
        if self.process.compiler.name:
            print "WARNING: Overwriting preexisting compiler name"
        self.process.compiler.name = verify_string(name)

    def modify_compiler_options(self, options):
        if self.process.compiler.options:
            print "WARNING: Overwriting preexisting compiler options"
        self.process.compiler.options = verify_string(options)


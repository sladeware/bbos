"""Class representing all that is required to operate a compiler.

The BBOS compiler class represents all that is required by compilers used to
build your application. Each core's compiler in the system may require
different arguments, executables, library paths, source files and include
paths in order to produce a binary for your process running on that core.
"""

__copyright__ = "Copyright (c) 2010 Slade Maurer, Alexander Sviridenko"

from bbos.builder.common import *


class BBOSCompiler:
    def __init__(self, base=None, defines=None, includes=None, include_argument=None, name=None, options=None):
        # The base directory for BBOS
        self.base = verify_string(base)

        # The list of compiler defines
        self.defines = verify_list(defines)

        # The list of include directories
        self.includes = verify_list(includes)

        # The argument used by the compiler for includes
        self.include_argument = verify_string(include_argument)

        # The name of the compiler binary
        self.name = verify_string(name)

        # The compiler options
        self.options = verify_list(options)

    def get_includes(self):
        include_string = ""
        for i in self.includes:
            include_string += self.include_argument + i + " "
        return include_string

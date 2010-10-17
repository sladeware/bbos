# 
# Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
#

from common import *

class BBOSCompiler:
    def __init__(self, base=None, includes=None, include_argument=None, name=None, options=None):
        # The base directory for BBOS
        self.base = verify_string(base)

        # The list of include directories
        self.includes = verify_list(includes)

        # The argument used by the compiler for includes
        self.include_argument = verify_string(include_argument)

        # The name of the compiler binary
        self.name = verify_string(name)

        # The compiler options
        self.options = verify_list(options)

    def get_includes(self):
        for i in self.includes:
            self.include_string += self.include_argument + " " + i + " "
        return self.include_string

    def get_options(self):
        for o in self.options:
            self.options_string += o + " "
        return self.options_string

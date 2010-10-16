# 
# Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
#

from types import *

class BBOSCompiler:
    def __init__(self, b, i, ia, n, o):
        # The base directory for BBOS
        self.base = b
        assert type(self.base) is StringType, "base is not a string type: %s" % self.base

        # The list of include directories
        self.includes = i
        assert type(self.includes) is ListType, "includes is not a list type: %s" % self.includes 

        # The argument used by the compiler for includes
        self.include_argument = ia
        assert type(self.include_argument) is StringType, "include_argument is not a string type: %s" % self.include_argument

        # The name of the compiler binary
        self.name = n
        assert type(self.name) is StringType, "name is not a string type: %s" % self.name

        # The compiler options
        self.options = o
        assert type(self.options) is ListType, "options is not a list type: %s" % self.options

    def get_includes(self):
        for i in includes:
            include_string += include_argument + " " + i + " "
        return include_string

    def get_options(self):
        for o in options:
            options_string += o + " "
        return options_string

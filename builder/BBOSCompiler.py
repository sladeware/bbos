# 
# Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
#

from types import *

class BBOSCompiler:
    def __init__(self, base, includes, include_argument, name, options):
        # The base directory for BBOS
        self.base = base
        assert type(self.base) is StringType, "base is not a string type: %s" % self.base

        # The list of include directories
        self.includes = includes
        assert type(self.includes) is ListType, "includes is not a list type: %s" % self.includes 

        # The argument used by the compiler for includes
        self.include_argument = include_argument
        assert type(self.include_argument) is StringType, "include_argument is not a string type: %s" % self.include_argument

        # The name of the compiler binary
        self.name = name
        assert type(self.name) is StringType, "name is not a string type: %s" % self.name

        # The compiler options
        self.options = options
        assert type(self.options) is ListType, "options is not a list type: %s" % self.options

    def get_includes(self):
        for i in self.includes:
            self.include_string += self.include_argument + " " + i + " "
        return self.include_string

    def get_options(self):
        for o in self.options:
            self.options_string += o + " "
        return self.options_string

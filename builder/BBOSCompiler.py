# 
# Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
#

from types import *

class BBOSCompiler:
    def __init__(self, base=None, includes=None, include_argument=None, name=None, options=None):
        # The base directory for BBOS
        self.base = base
        assert type(self.base) in (StringType, NoneType), "base is not a string type: %s" % self.base

        # The list of include directories
        self.includes = includes
        assert type(self.includes) in (ListType, NoneType), "includes is not a list type: %s" % self.includes 

        # The argument used by the compiler for includes
        self.include_argument = include_argument
        assert type(self.include_argument) in (StringType, NoneType), "include_argument is not a string type: %s" % self.include_argument

        # The name of the compiler binary
        self.name = name
        assert type(self.name) in (StringType, NoneType), "name is not a string type: %s" % self.name

        # The compiler options
        self.options = options
        assert type(self.options) in (ListType, NoneType), "options is not a list type: %s" % self.options

    def get_includes(self):
        for i in self.includes:
            self.include_string += self.include_argument + " " + i + " "
        return self.include_string

    def get_options(self):
        for o in self.options:
            self.options_string += o + " "
        return self.options_string

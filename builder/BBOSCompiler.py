# 
# Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
#

from types import *

class BBOSCompiler:
    # The base directory for BBOS
    base = None

    # The list of include directories
    includes = None

    # The argument used by the compiler for includes
    include_argument = None
    
    # The name of the compiler binary
    name = None

    # The compiler options
    options = None
    
    def __init__(self, b, i, ia, n, o):
        base = b
        assert type(base) is StringType, "base is not a string type: %s" % base
        includes = i
        assert type(includes) is ListType, "includes is not a list type: %s" % includes 
        include_argument = ia
        assert type(include_argument) is StringType, "include_argument is not a string type: %s" % include_argument
        name = n
        assert type(name) is StringType, "name is not a string type: %s" % name
        options = o
        assert type(options) is ListType, "options is not a list type: %s" % options

    def get_includes(self):
        for i in includes:
            include_string += include_argument + " " + i + " "
        return include_string

    def get_options(self):
        for o in options:
            options_string += o + " "
        return options_string

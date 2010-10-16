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
    
    def __init__(b, i, ia, n, o):
        base = b
        assert type(base) is StringType, "base is not a string type"
        includes = i
        assert type(includes) is ListType, "includes is not a list type"
        include_argument = ia
        assert include_argument is StringType, "include_argument is not a string type"
        name = n
        assert type(name) is StringType, "name is not a string type"
        options = o
        assert type(options) is ListType, "options is not a list type"

    def get_includes():
        for i in includes:
            include_string += include_argument + " " + i + " "
        return include_string

    def get options():
        for o in options:
            options_string += o + " "
        return options_string

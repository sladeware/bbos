from types import *

class BBOSDriver:
    # This is the main entry function for the driver that calls messenger()
    entry_function = None

    # The driver source files
    files = None

    # The unique name of this driver
    name = None

    # The number of the port used for communication with this driver
    port = None

    # The version of the driver
    version = None

    def __init__(e, f, n, p, v):
        entry_function = e
        assert type(entry_function) is StringType, "entry_function is not a string type"
        files = f
        assert type(files) is ListType, "files is not a list type"
        name = n
        assert type(name) is StringType, "name is not a string type"
        port = p
        assert type(port) is IntegerType, "port is not an integer type"
        version = v
        assert type(version) is IntegerType, "version is not an integer type"

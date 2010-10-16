from types import *

class BBOSApplication:
    # The list of processes within this application
    processes = None

    def __init__(p):
        processes = p
        assert type(processes) is ListType, "processes is not a list type"

"""Common subroutines used within the BBOS builder.
"""

__copyright__ = "Copyright (c) 2010 Slade Maurer, Alexander Sviridenko"

from types import *

# This is the C header file we are code generating that connects it all together
BBOS_HEADER = "/bbos.h"

# System thread names
BBOS_IDLE_THREAD_NAME = "bbos_idle"
BBOS_IPC_THREAD_NAME = "bbos_ipc"

def verify_boolean(var):
    if var:
        assert type(var) is BooleanType, "%s is not a boolean type: %s" % (var.__name__, var)
    return var

def verify_int(var):
    if var:
        assert type(var) is IntType, "%s is not a int type: %s" % (var.__name__, var)
    return var

def verify_list(var):
    if var:
        assert type(var) is ListType, "%s is not a list type: %s" % (var.__name__, var)
    return var

def verify_string(var):
    if var:
        assert type(var) is StringType, "%s is not a string type: %s" % (var.__name__, var)
    return var



# 
# Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
#
# Common subroutines used within the BBOS builder.
#

from types import *

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



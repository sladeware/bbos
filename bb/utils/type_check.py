#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

"""Validation tools for generic object structures."""

from types import *

def is_int(var):
    """Return true if the specified object is an integer."""
    return type(var) is IntType

def is_long(var):
    """Return true if the specified object is a long integer."""
    return type(var) is LongType

def is_boolean(var):
    """Return true if the specified object is a boolean."""
    return type(var) is BooleanType

def is_string(var):
    """Return true if the specified object is a string."""
    return type(var) is StringType

def is_list(var):
    """Return true if the specified variable is a list."""
    return type(var) is ListType

def is_tuple(var):
    return type(var) is TupleType

def is_dict(var):
    """Return true if the specified variable is a dictionary."""
    return type(var) is DictType

def verify_boolean(var):
    if var and not is_boolean(var):
        raise TypeError("'%s' is not a boolean type: %s" %
                        (var.__class__.__name__, var))
    return var

def verify_int(var):
    if var and not is_int(var):
        raise TypeError("'%s' is not a int type: %s" %
                        (var.__class__.__name__, var))
    return var

def verify_list(var):
    if var and not is_list(var):
        raise TypeError("'%s' is not a list type: %s" %
                        (var.__class__.__name__, var))
    return var

def verify_string(var):
    if not var or not is_string(var):
        raise TypeError("'%s' is not a string type: %s" %
                        (var.__class__.__name__, var))
    return var

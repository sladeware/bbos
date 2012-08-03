#!/usr/bin/env python

import inspect
import types

def is_class(var):
    return inspect.isclass(var)

def is_int(var):
  """Return ``True`` if the specified object is an integer."""
  return type(var) is types.IntType

def is_long(var):
  """Return true if the specified object is a long integer."""
  return type(var) is types.LongType

def is_boolean(var):
  """Return true if the specified object is a boolean."""
  return type(var) is types.BooleanType

is_bool = is_boolean

def is_string(var):
  """Return true if the specified object is a string."""
  return type(var) is types.StringType

def is_list(var):
  """Return true if the specified variable is a list."""
  return type(var) is types.ListType

def is_function(var):
  return type(var) is types.FunctionType

def is_tuple(var):
  return type(var) is types.TupleType

def is_dict(var):
  """Return true if the specified variable is a dictionary."""
  return type(var) is types.DictType

def is_number(x):
  "Is x a number? We say it is if it has a __int__ method."
  return hasattr(x, '__int__')

def is_sequence(x):
  "Is x a sequence? We say it is if it has a __getitem__ method."
  return hasattr(x, '__getitem__')

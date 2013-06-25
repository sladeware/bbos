# -*- coding: utf-8; -*-
#
# http://www.bionicbunny.org/
# Copyright (c) 2013 Sladeware LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This module provides set of type cheching utils."""

import inspect
import types

def is_class(obj):
  """Returns ``True`` if the specified object is class."""
  return inspect.isclass(obj)

def is_int(obj):
  """Returns ``True`` if the specified object is integer."""
  return type(obj) is types.IntType

def is_long(obj):
  """Returns ``True`` if the specified object is long integer."""
  return type(obj) is types.LongType

def is_boolean(obj):
  """Returns ``True`` if the specified object is boolean."""
  return type(obj) is types.BooleanType

def is_string(obj):
  """Returns ``True`` if the specified object is a string."""
  return type(obj) is types.StringType

def is_list(obj):
  """Returns ``True`` if the specified object is a list."""
  return type(obj) is types.ListType

def is_function(obj):
  """Returns ``True`` if object is a function."""
  return type(obj) is types.FunctionType

def is_tuple(obj):
  """Returns ``True`` if object is a tuple."""
  return type(obj) is types.TupleType

def is_dict(obj):
  """Returns ``True`` if the specified object is a dictionary."""
  return type(obj) is types.DictType

def is_number(x):
  """Is `x` a number? We say it is if it has a ``__int__`` method."""
  return hasattr(x, "__int__")

def is_sequence(x):
  """Is `x` a sequence? We say it is if it has a ``__getitem__`` method."""
  return hasattr(x, "__getitem__")

# Aliases
is_bool = is_boolean
is_callable = callable
is_func = is_function

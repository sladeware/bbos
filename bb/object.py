#!/usr/bin/env python
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

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

# TODO: save original classmethod()

import __builtin__
import types
import inspect

from bb.utils import typecheck

METHODS = {}

def get_all_subclasses(cls):
  """Returns all subclasses."""
  if not typecheck.is_class(cls):
    return []
  return list(cls.__bases__) + [g for s in cls.__bases__
                                for g in get_all_subclasses(s)]

class methodwrapper(object):

  def __init__(self, func):
    global METHODS
    self._cases = {}
    mod = inspect.getmodule(func)
    record = inspect.getouterframes(inspect.currentframe())[1]
    (frame, filename, lineno, funcname, codecontext, index) = record
    key = (mod and mod.__name__ or None, funcname, func.__name__)
    if key in METHODS:
      _method, _func = METHODS[key]
      self.set_method(_func, _method)
    self.set_method(func)
    METHODS[key] = (self, func)

  def set_method(self, func, method=None):
    if not method:
      method = self
    self._cases[method.__class__] = func

  def __get__(self, object_, class_=None):
    if object_:
      func = self._cases[instancemethod]
      return types.MethodType(func, object_, class_)
    else:
      func = self._cases[classmethod]
      return types.MethodType(func, class_)

class classmethod(methodwrapper):
  """New :func:`classmethod`."""
  pass

__builtin__.classmethod = classmethod

class instancemethod(methodwrapper):
  pass

__builtin__.instancemethod = instancemethod

class CloneNotImplementedError(Exception):
  pass

class Cloneable:
  """This (empty) interface must be implemented by all classes that wish to
  support cloning. The implementation of clone() in Object checks if the object
  being cloned implements this interface and throws CloneNotSupportedError if it
  does not.
  """

  def clone(self):
    """Creates and returns a copy of the object."""
    raise CloneNotImplementedError()

class Object(object):
  """The main object class of the BB hierarchy."""

  Cloneable = Cloneable

  def get_class(self):
    """Returns the unique instance of class that represents this object's
    class.
    """
    return self.__class__

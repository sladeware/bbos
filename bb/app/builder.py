#!/usr/bin/env python
#
# http://bionicbunny.org/
# Copyright (c) 2012 Sladeware LLC
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

import inspect

import bb
from bb import host_os
from bb.app.object import Object
from bb.tools import compiler_manager
from bb.tools.compilers.compiler import Compiler, CompilerParameters
from bb.utils import typecheck

class ObjectHandler(object):

  def __init__(self, f):
    self._function = f
    self._object = None

  def set_object(self, obj):
    self._object = obj

  def __call__(self, *args, **kwargs):
    ext_args = args + (self._object,)
    return self._function(*ext_args, **kwargs)

class Builder(bb.Object, bb.Object.Cloneable):
  """Builder builds particular :class:`bb.app.object.Object`."""

  COMPILER_PARAMS = {}

  def __init__(self, obj=None):
    bb.Object.__init__(self)
    self._object = None
    self._selected_compiler = None
    self._compiler_params = {}
    self._object_handlers = []
    for compiler_class, params in self.COMPILER_PARAMS.items():
      self.add_compiler_params(params)
    if obj:
      self.set_object(obj)

  def __iadd__(self, obj):
    if isinstance(obj, CompilerParameters):
      self.add_compiler_params(obj)
    return self

  def __str__(self):
    return "%s[obj_class=%s]" % \
        (self.__class__.__name__,
         self._object and self._object.__class__.__name__ or None)

  def __call__(self, f):
    # TODO: provide additional method, so user will be able manually bind
    # function to builder, e.g. builder.add_object_handler(f).
    handler = ObjectHandler(f)
    self.add_object_handler(handler)
    return handler

  def add_object_handlers(self, handlers):
    for handler in handlers:
      self.add_object_handler(handler)

  def add_object_handler(self, handler):
    if handler in self._object_handlers:
      return
    self._object_handlers.append(handler)

  def get_object_handlers(self):
    return self._object_handlers

  def set_object(self, obj):
    if typecheck.is_class(obj):
      if not issubclass(obj, Object):
        raise TypeError("'obj' has to be subclass of Object")
    elif not isinstance(obj, Object):
      raise TypeError("'obj' has to be derived from Object: %s" % obj)
    self._object = obj

  def get_object(self):
    """Returns :class:`bb.application.object.Object` that is source for this
    builder.
    """
    return self._object

  def clone(self):
    """Copies builder and returns :class:`Builder` clone."""
    builder = self.__class__()
    if self.get_selected_compiler():
      builder.select_compiler(self.get_selected_compiler())
    builder.read_compiler_params(self.get_compilers_params())
    builder.add_object_handlers(self.get_object_handlers())
    return builder

  def _read_compiler_params_from_dict(self, d):
    if not typecheck.is_dict(d):
      raise TypeError("'d' is not dict")
    caller_frame = inspect.getouterframes(inspect.currentframe(), 2)
    filename = inspect.getsourcefile(caller_frame[2][0])
    for name, params in d.items():
      # TODO: allow more cases
      if not typecheck.is_string(name):
        raise TypeError("Compiler name has to be represented by string")
      compiler_class = compiler_manager.identify_compiler(name)
      if not compiler_class:
        raise Exception("No such compiler: %s" % name)
      params_class = compiler_class.Parameters
      params = params_class(params)
      params.__file__ = filename
      self.add_compiler_params(params)

  def read_compiler_parameters(self, *args, **kwargs):
    """Reads compiler params in different ways."""
    caller_frame = inspect.getouterframes(inspect.currentframe(), 2)
    basedir = host_os.path.dirname(inspect.getsourcefile(caller_frame[1][0]))
    if not len(kwargs) and len(args) == 1:
      if typecheck.is_list(args[0]):
        for params in args[0]:
          self.add_compiler_params(params)
      elif typecheck.is_dict(args[0]):
        self._read_compiler_params_from_dict(args[0])
    elif not len(args) and len(kwargs):
      self._read_compiler_params_from_dict(kwargs)
    else:
      raise NotImplementedError()

  read_compiler_params = read_compiler_parameters

  def select_compiler(self, compiler):
    """Selectes compiler if it is in the list of supported compilers. Returns
    whether or not compiler was selected.

    Selected compiler will be used by such methods as
    :func:`get_compiler_params`.
    """
    if not isinstance(compiler, Compiler):
      raise TypeError("'compiler' has to be an instance of Compiler")
    if not compiler.__class__ in self.get_supported_compilers():
      return False
    self._selected_compiler = compiler
    return True

  def get_selected_compiler(self):
    """Returns selected compiler."""
    return self._selected_compiler

  def build(self, obj):
    compiler = self.get_selected_compiler()
    if not compiler:
      raise Exception("Please select compiler")
    for handler in self.get_object_handlers():
      handler.set_object(obj)
    params = self.get_compiler_params()
    compiler.read_options(params)

  def get_supported_compilers(self):
    """Returns list of supported compilers. See also
    :func:`get_compiler_params`.
    """
    supported_compilers = self._compiler_params.keys()
    if None in supported_compilers:
      supported_compilers.remove(None)
    return supported_compilers

  def add_compiler_params(self, params):
    """Adds compiler params derived from :class:`CompilerParameters`."""
    if not params or not isinstance(params, CompilerParameters):
      raise TypeError("'params' has to be derived from CompilerParameters: %s" %
                      params)
    compiler_class = params.COMPILER_CLASS
    if compiler_class in self._compiler_params:
      self._compiler_params[compiler_class].merge(params)
    else:
      self._compiler_params[compiler_class] = params

  def get_compiler_params(self, compiler=None):
    if compiler:
      compiler = compiler_manager.identify_compiler(compiler)
    elif self.get_selected_compiler():
      compiler = self._selected_compiler.__class__
    return self._compiler_params.get(compiler, None)

  def get_compilers_params(self):
    return self._compiler_params.values()

def builder_class_factory(object_class):
  def __init__(self, *args, **kwargs):
    Builder.__init__(self, *args, **kwargs)
  dict_ = {
    "__init__": __init__,
    "__module__": object_class.__module__,
    "__iadd__": Builder.__iadd__
    }
  builder_class = type("%s%s" % (object_class.__name__, Builder.__name__),
                       (Builder,), dict_)
  return builder_class

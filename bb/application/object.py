#!/usr/bin/env python
#
# http://bionicbunny.org
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

import types

import bb
import bb.object
from bb.utils import typecheck
from bb.utils import pyimport
from bb.tools import compiler_manager
from bb.tools.compilers.compiler import CompilerParameters

class _MetaBuilder(type):

  def __iadd__(self, object_):
    if isinstance(object_, CompilerParameters):
      self.add_compiler_params(object_)
    return self

class Builder(object):

  __metaclass__ = _MetaBuilder

  COMPILER_PARAMS = {}

  def __init__(self, obj):
    if not isinstance(obj, Buildable):
      raise TypeError()
    self._object = obj
    self._selected_compiler = None
    self._compiler_params = {}
    for compiler_class, params in self.COMPILER_PARAMS.items():
      self.add_compiler_params(params)

  def select_compiler(self, compiler):
    class_ = compiler_manager.identify_compiler(compiler)
    self._selected_compiler = class_

  def get_supported_compilers(self):
    supported_compilers = self._compiler_params.keys()
    if None in supported_compilers:
      supported_compilers.remove(None)
    return supported_compilers

  @instancemethod
  def add_compiler_params(self, params):
    compiler_class = params.COMPILER_CLASS
    self._compiler_params[compiler_class] = params

  @classmethod
  def add_compiler_params(klass, params):
    if not isinstance(params, CompilerParameters):
      raise TypeError()
    compiler_class = params.COMPILER_CLASS
    klass.COMPILER_PARAMS[compiler_class] = params

  def get_compiler_params(self, compiler=None):
    compiler = compiler or self._selected_compiler
    return self._compiler_params.get(compiler, None)

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

class Buildable(object):
  """This interface ties Object with Builder."""

  BUILDER_CLASS = None

  def __init__(self):
    self.__builder = None
    if not self.BUILDER_CLASS:
      raise NotImplementedError()
    self.__builder = self.BUILDER_CLASS(self)

  @classmethod
  def get_builder(klass):
    return klass.BUILDER_CLASS

  @instancemethod
  def get_builder(self):
    return self.__builder

class MetaObject(type):

  def __new__(metaclass, name, bases, dictionary):
    object_class = type.__new__(metaclass, name, bases, dictionary)
    subclasses = bb.object.get_all_subclasses(object_class)
    if Buildable in subclasses:
      builder_class = builder_class_factory(object_class)
      object_class.Builder = object_class.BUILDER_CLASS = builder_class
    return object_class

class Object(bb.Object):
  """This object class is derived from :class:`bb.object.Object` and has to be
  used as a basis for any application object.
  """

  Buildable = Buildable

  __metaclass__ = MetaObject

  def __init__(self):
    if Buildable in bb.object.get_all_subclasses(self.__class__):
      Buildable.__init__(self)

def _catch_builder_import():
  """
    from bb.os import OS, OSBuilder
  """
  def ensure_fromlist(self, m, fromlist, recursive=0):
    try:
      pyimport.ModuleImporter.ensure_fromlist(self, m, fromlist, recursive)
    except ImportError, e:
      if not m.__name__ == "bb" and not m.__name__.startswith("bb."):
        raise ImportError(e)
      for name in fromlist:
        if name.endswith(Builder.__name__):
          obj = getattr(m, name[:len(name) - len(Builder.__name__)], None)
          if not obj:
            raise
          setattr(m, name, get_builder(obj))
  importer = pyimport.get_importer()
  importer.ensure_fromlist = types.MethodType(ensure_fromlist, importer)

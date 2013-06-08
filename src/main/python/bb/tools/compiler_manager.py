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

from distutils import fancy_getopt
import inspect
import sys

import bb
from bb.tools.compilers.compiler import Compiler
from bb.utils import typecheck

COMPILERS_PACKAGE = "bb.tools.compilers"
_COMPILER_CLASSES = dict()

def _fix_compiler_name(name):
  if not typecheck.is_string(name):
    raise TypeError("Compiler's name must be a string")
  return name.lower()

def identify_compiler(object_):
  if typecheck.is_string(object_):
    return _COMPILER_CLASSES.get(object_, None)
  elif typecheck.is_class(object_):
    if _fix_compiler_name(object_.__name__) in _COMPILER_CLASSES:
      return _COMPILER_CLASSES[_fix_compiler_name(object_.__name__)]
  elif isinstance(object_, Compiler):
    return identify_compiler(object_.__class__)
  return None

def new_compiler(name, args={}):
  """Returns :class:`Compiler` instance. Returns ``None`` if compiler is not
  supported.
  """
  if not typecheck.is_string(name):
    raise Exception("Must be string")
  name = _fix_compiler_name()
  class_ = _COMPILER_CLASSES.get(name, None)
  if not class_:
    print "Compiler '%s' is not supported" % name
    return None
  return class_(**args)

def show_compilers():
  """Print list of available compilers."""
  compilers = []
  for name, class_ in _COMPILER_CLASSES.items():
    compilers.append(("compiler=" + name, None, ""))
  compilers.sort()
  pretty_printer = fancy_getopt.FancyGetopt(compilers)
  pretty_printer.print_help("List of available compilers:")

def _init():
  classes = inspect.getmembers(sys.modules[COMPILERS_PACKAGE], inspect.isclass)
  for name, klass in classes:
    if klass is Compiler:
      continue
    if issubclass(klass, Compiler):
      _COMPILER_CLASSES[_fix_compiler_name(klass.__name__)] = klass

def main():
  # print _COMPILER_CLASSES
  show_compilers()
  return 0

_init()
if __name__ == "__main__":
  exit(main())

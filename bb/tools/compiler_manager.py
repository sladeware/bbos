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

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'
__author__ = 'Oleksandr Sviridenko'

import inspect
import sys

import bb
from bb.tools.compilers import Compiler
from bb.lib.utils import typecheck

_COMPILER_CLASSES = dict()

def new_compiler(name, args={}):
  """Returns Compiler instance. Returns None if compiler is not supported."""
  if not typecheck.is_string(name):
    raise Exception("Must be string")
  name = name.upper()
  compiler_class = _COMPILER_CLASSES.get(name, None)
  if not compiler_class:
    print "Compiler '%s' is not supported" % name
    return None
  return compiler_class(**args)

def _init():
  classes = inspect.getmembers(sys.modules['bb.tools.compilers'],
                               inspect.isclass)
  for name, klass in classes:
    if klass is Compiler:
      continue
    if issubclass(klass, Compiler) and klass.get_name():
      _COMPILER_CLASSES[klass.get_name().upper()] = klass

_init()

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

import inspect
import sys

import bb
from bb.tools.toolchains import Toolchain
from bb.utils import typecheck

_toolchain_classes = dict()

classes = inspect.getmembers(sys.modules['bb.tools.toolchains'],
                             inspect.isclass)
for name, klass in classes:
  if klass is Toolchain:
    continue
  if issubclass(klass, Toolchain):
    _toolchain_classes[name.upper()] = klass

def is_supported_toolchain(name):
  return get_toolchain_class(name) != None

def new_toolchain(name, args={}):
  toolchain_class = get_toolchain_class(name)
  if not toolchain_class:
    print "Toolchain '%s' is not supported" % name
    return None
  return toolchain_class(**args)

def get_toolchain_class(name):
  global _toolchain_classes
  if not typecheck.is_string(name):
    raise Exception("Must be string")
  name = name.upper()
  return _toolchain_classes.get(name, None)

def get_toolchain_classes():
  global _toolchain_classes
  return _toolchain_classes.values()

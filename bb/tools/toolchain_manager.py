#!/usr/bin/env python

import inspect
import sys

import bb
from bb.lib.build.toolchains import Toolchain
from bb.lib.utils import typecheck

_toolchain_classes = dict()

classes = inspect.getmembers(sys.modules['bb.lib.build.toolchains'], inspect.isclass)
for name, klass in classes:
  if klass is Toolchain:
    continue
  if issubclass(klass, Toolchain):
    _toolchain_classes[name.upper()] = klass

def is_supported_toolchain(name):
  return get_toolchain_class(name) != None

def new_toolchain(name, args={}):
  toolchain_class = get_toolchain_class(name)
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

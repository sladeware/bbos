#!/usr/bin/env python

import inspect
import sys

import bb
from bb.tools.toolchains import Toolchain
from bb.lib.utils import typecheck

_toolchains = dict()

classes = inspect.getmembers(sys.modules['bb.tools.toolchains'], inspect.isclass)
for name, klass in classes:
    if klass is Toolchain:
        continue
    if issubclass(klass, Toolchain):
        _toolchains[name.upper()] = klass

def get_toolchain(name):
    global _toolchains
    if not typecheck.is_string(name):
        raise Exception("Must be string")
    name = name.upper()
    return _toolchains.get(name, None)

def get_toolchains():
    global _toolchains
    return _toolchains.values()

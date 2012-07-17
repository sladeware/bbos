#!/usr/bin/env python

import inspect
import sys

from bb.build.toolchains import Toolchain
from bb.lib.utils import typecheck

_toolchains = dict()

# Register existed toolchains
classes = inspect.getmembers(sys.modules['bb.build.toolchains'], inspect.isclass)
for name, klass in classes:
    if klass is Toolchain:
        continue
    if issubclass(klass, Toolchain):
        _toolchains[name.upper()] = klass

def get_toolchain_class_by_name(name):
    if not typecheck.is_string(name):
        raise Exception("Must be string")
    name = name.upper()
    return _toolchains.get(name, None)

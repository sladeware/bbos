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

import os # this is host-os support module, do not mix with bb.os
import inspect
import sys

import bb.config.py_import # override standard __import__

# Setup host environment, check compatibility and some dependencies

# TODO: choose the right names

os.environ['BB_HOME'] = \
  os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../.."))

bb_package_file = inspect.getsourcefile(sys.modules['bb'])
bb_package_dir = os.path.abspath(os.path.join(os.path.dirname(bb_package_file),
                                              '..'))
os.environ['BB_PACKAGE_HOME'] = bb_package_dir
os.environ['BB_APPLICATION_HOME'] = os.path.dirname(os.path.join(sys.path[0],
                                                                 sys.argv[0]))


# Compatibility with Python 2.5 through 2.7.
assert (2,5) <= sys.version_info < (3,), """\
This code is meant for Python 2.5 through 2.7.
You might find that the parts you care about still work in older
Pythons or happen to work in newer ones, but you're on your own --
edit __init__.py if you want to try it."""

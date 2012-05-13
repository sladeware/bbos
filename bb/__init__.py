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

from __future__ import absolute_import

__copyright__ = "Copyright (c) 2011-2012 Sladeware LLC"

import os # this is host-os support module, do not mix with bb.os
import sys

#_______________________________________________________________________________
# Setup host environment, check compatibility and some dependencies

os.environ["BB_HOME"] = \
  os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))

# Compatibility with Python 2.5 through 2.7.
assert (2,5) <= sys.version_info < (3,), """\
This code is meant for Python 2.5 through 2.7.
You might find that the parts you care about still work in older
Pythons or happen to work in newer ones, but you're on your own --
edit __init__.py if you want to try it."""

#_______________________________________________________________________________
# Do general imports and create common aliases

from bb.app import Mapping, mapping_factory
from bb.os import OS

BBOS = OS

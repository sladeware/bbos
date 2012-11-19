#!/usr/bin/env python
#
# http://bionicbunny.org/
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

"""This module is wrapper for internal :mod:`os` and provides a portable way of
using host operating system dependent functionality.

To make :mod:`os` package available, BB creates an alias such as
:mod:`bb.host_os`.
"""

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

import inspect
# TODO: use bb.utils.module instead of the implementation below.
from os import *
import platform
import sys

from bb.host_os import path

BB_HOME_DIR = path.absjoin(path.dirname(path.realpath(__file__)), "..")
BB_PKG_FILE = inspect.getsourcefile(sys.modules["bb"])
BB_PKG_DIR = path.absjoin(path.dirname(BB_PKG_FILE), "..", "bb")

class Environment(dict):
  """Another version of :var:`os.environ` with a few features."""

  def __init__(self):
    dict.__init__(self)

  def get(self, key, default_value=None):
    return environ.get(key, default_value)

  def echo(self, key, default_value=None):
    print self.get(key, default_value)

  def pwd(self):
    f = caller(n=2)
    return path.dirname(inspect.getfile(f))

  def __setitem__(self, key, value):
    environ[key] = value

  def __getitem__(self, key):
    return self.get(key)

env = Environment()

env["OS_NAME"] = platform.system() # NOTE: what about os.name?
env["PROCESSOR_NAME"] = platform.processor()
env["ARCH_NAME"] = platform.machine()
env.setdefault("BB_HOME_DIR", BB_HOME_DIR)
env["BB_PKG_DIR"] = BB_PKG_DIR

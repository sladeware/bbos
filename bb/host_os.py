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

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

import inspect
# TODO: use bb.utils.module instead of the following implementation.
from os import *

class _Environment(dict):
  """Another version of os.environ with a few features."""

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

env = _Environment()

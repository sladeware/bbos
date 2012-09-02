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

class Port(object):
  """Thread communication technique. At some point, this is just a protected
  messaging pool for communication between threads.

  Each port has a ``name`` and ``capacity``, or how many messages it can keep.
  """

  def __init__(self, capacity):
    assert capacity > 0, "Port capacity must be greater than zero"
    self._capacity = capacity

  def get_capacity(self):
    return self._capacity

  def __str__(self):
    return "%s[capacity=%d]" % (self.__class__.__name__, self.get_capacity())

# -*- coding: utf-8; -*-
#
# Copyright (c) 2012-2013 Sladeware LLC
# http://www.bionicbunny.org/
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

"""Thread communication technique. At some point, this is just a protected
messaging pool for communication between threads.

All the ports are registered within a :class:`~bb.app.mapping.Mapping` with help
of :func:`~bb.app.mapping.Mapping.register_port` method.
"""

from bb.utils import typecheck

class Port(object):
  """This class represents a port, which will be used for message passing
  communication purposes.

  :param capacity: An integer that defines how many messages this port can keep.
  :param name optional: A string that represents port name.
  """

  name_format = '%s_port'

  def __init__(self, capacity, name=None):
    if capacity < 1:
      raise Exception("Port capacity must be greater than zero")
    self._name = None
    self._uid = 0
    self._capacity = 0
    self._set_capacity(capacity)

  def _set_uid(self, uid):
    if not isinstance(uid, int):
      raise TypeError()
    self._uid = uid

  def get_uid(self):
    """Returns port's UID."""
    return self._uid

  def set_name(self, name):
    """Set port name."""
    if not typecheck.is_string(name):
      raise TypeError("name must be a string")
    self._name = name

  def get_name(self):
    return self._name

  def _set_capacity(self, n):
    """Set port capacity.

    :param n: Max number of messages.
    """
    if not type(n) in (int, long):
      raise TypeError()
    self._capacity = n

  def get_capacity(self):
    """Returns port capacity value."""
    return self._capacity

  def __str__(self):
    return "%s[name=%s, capacity=%d]" % (self.__class__.__name__,
                                         self.get_name(), self.get_capacity())

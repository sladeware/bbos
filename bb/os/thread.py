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

import bb
from bb.lib.utils import typecheck
from bb.os.port import Port

class Thread(bb.Object):
  """The thread is an atomic unit action within the BB operating system, which
  describes application specific actions wrapped into a single context of
  execution.

  The order of ports is important here. The first port (0) always counts as
  default one.
  """

  NAME = None
  NAME_FORMAT = 'THREAD_%d'
  RUNNER = None
  PORTS = []

  def __init__(self, name=None, runner=None, ports=[]):
    bb.Object.__init__(self)
    self._name = None
    self._name_format = None
    self._runner = None
    self._ports = []
    if name:
      self.set_name(name)
    elif getattr(self, 'NAME', None) is not None:
      self.set_name(getattr(self, 'NAME'))
    if runner:
      self.set_runner(runner)
    elif hasattr(self, "RUNNER"):
      self._runner = self.RUNNER
    else:
      raise Exception("Runner wasn't provided")
    if hasattr(self, 'PORTS'):
      self.add_ports(self.PORTS)
    if ports:
      self.add_ports(ports)
    if hasattr(self, 'NAME_FORMAT'):
      self._name_format = getattr(self, 'NAME_FORMAT')

  def get_name_format(self):
    return self._name_format

  def set_name_format(self, frmt):
    if not typecheck.is_string(frmt):
      raise TypeError('Name format must be string')
    self._name_format = frmt

  def set_runner(self, runner):
    if not typecheck.is_string(runner):
      raise TypeError('Must be string')
    self._runner = runner

  def get_runner(self):
    return self._runner

  def set_name(self, name):
    if not name:
      raise TypeError('Name cannot be None value')
    if not typecheck.is_string(name):
      raise TypeError('Must be string')
    self._name = name

  def get_name(self):
    return self._name

  def add_ports(self, ports):
    if not typecheck.is_sequence(ports):
      raise TypeError("ports must be a sequence of bb.os.port.Port instances.")
    for port in ports:
      self.add_port(port)
    return self

  def has_port(self, port):
    if not isinstance(port, Port):
      raise TypeError("port must be derived from bb.os.port.Port")
    return port in self.get_ports()

  def add_port(self, port, default=False):
    """Add port to the sequence of ports controled by this thread. Optionally
    can be set as default port (by default is Flase). Note, the first port
    always counts as default one.

    In case you need to make already added port as default, just add this port
    once again and set default as True.
    """
    if not isinstance(port, Port):
      raise TypeError("port must be derived from bb.os.port.Port")
    if self.has_port(port) and default is False:
      return self
    if self.get_num_ports() and default is True:
      if self.has_port(port):
        self._ports.remove(port)
      self._ports = [port] + self._ports
      return self
    self._ports.append(port)
    return self

  def remove_all_ports(self):
    self._ports = []

  def get_default_port(self):
    """Return default port for this thread. Return None if no ports presented.
    """
    if not self.get_num_ports():
      return None
    return self.get_ports()[0]

  def get_ports(self):
    return self._ports

  def get_num_ports(self):
    return len(self.get_ports())

  def __str__(self):
    return "%s[name=%s, runner=%s]" % (self.__class__.__name__, self.get_name(),
                                       self.get_runner())

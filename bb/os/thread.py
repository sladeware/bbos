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
from bb.os.message import Message

class Thread(bb.Object):
  """The thread is an atomic unit action within the BB operating system, which
  describes application specific actions wrapped into a single context of
  execution.
  """

  NAME = None
  NAME_FORMAT = 'THREAD_%d'
  RUNNER = None
  PORT = None

  def __init__(self, name=None, runner=None, port=None, messages=[]):
    bb.Object.__init__(self)
    self._name = None
    self._name_format = None
    self._runner = None
    self._messages = {}
    self._port = None
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
    if not getattr(self, 'PORT', None) is None:
      self.set_port(self.PORT)
    if port:
      self.set_port(port)
    if hasattr(self, 'NAME_FORMAT'):
      self._name_format = getattr(self, 'NAME_FORMAT')

  def register_message(self, message):
    if not isinstance(message, Message):
      raise TypeError('message has to be derived from class Message.')
    if message.id in self._messages:
      return False
    self._messages[message.id] = message
    return True

  def get_supported_messages(self):
    """Return list of supported messages."""
    return self._messages.values()

  def unregister_message(self, message):
    if not isinstance(message, Message):
      raise TypeError('message has to be derived from class Message.')
    if message.id not in self._messages:
      return
    del self._messages[message.id]

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

  def has_port(self):
    return not self.get_port() is None

  def set_port(self, port):
    if not port or not isinstance(port, Port):
      raise TypeError("port must be derived from bb.os.port.Port")
    if self.has_port():
      self.remove_port()
    self._port = port
    return self

  def remove_port(self):
    self._port = None

  def get_port(self):
    return self._port

  def __str__(self):
    return "%s[name=%s, runner=%s, port=%s]" % (self.__class__.__name__,
                                                 self.get_name(),
                                                 self.get_runner(),
                                                 self.get_port())

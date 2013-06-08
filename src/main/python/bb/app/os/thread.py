# Copyright (c) 2012-2013 Sladeware LLC
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
#
# Author: Oleksandr Sviridenko

"""The multi-tasking BBOS kernel is responsible for the management of tasks and
communication between them. In BBOS terms these tasks are called `threads`. The
thread is an atomic unit of action within the BBOS operating system, which
describes application specific actions wrapped into a single context of
execution.

A thread is represented by the :class:`Thread`. This class represents
computation performed by an independent context of execution.

Let's take a look at an example to make this more clear. The following code
snippet creates a new thread, whose target is the function ``hello_world``::

  def hello_world():
    print 'Hello world!'

  hello = m.register_thread(Thread('HELLO', hello_world))

Now we have a thread called ``HELLO`` that handles our function
``hello_world``. Within BBOS such a function is called the thread's `entry
point` (or simply `runner`).
"""

from bb.app.os.port import Port
from bb.app.os.message import Message
from bb.utils import typecheck

class Thread(object):
  """The thread is an atomic unit action within the BB operating system, which
  describes application specific actions wrapped into a single context of
  execution.

  :param name: A string that represents thread's name.
  :param runner: A string that represents function name.
  :param port: A :class:`Port` instance that will be used for messaging.
  :param messages: A list of :class:`Message` instances.
  """

  name = None
  name_format = "THREAD_%d"
  runner = None
  port = None

  def __init__(self, name=None, runner=None, port=None, messages=[]):
    self._uid = None
    self._name = None
    self._name_format = None
    self._runner = None
    self._messages = {}
    self._port = None
    if name or getattr(self.__class__, "name", None):
      self.set_name(name or self.__class__.name)
    if runner or getattr(self.__class__, "runner", None):
      self.set_runner(runner or self.__class__.runner)
    if port or getattr(self.__class__, "port", None):
      self.set_port(port or self.__class__.port)
    if hasattr(self.__class__, "name_format"):
      self._name_format = getattr(self.__class__, "name_format")

  def _set_uid(self, uid):
    if not isinstance(uid, int):
      raise TypeError()
    self._uid = uid

  def get_uid(self):
    return self._uid

  def register_message(self, message):
    """Registers message so that OS will know that this thread will send/receive
    the message.

    :param message: A :class:`Message` derived instance.

    :raises: TypeError
    """
    if not isinstance(message, Message):
      raise TypeError('message has to be derived from class Message: %s' \
                        % type(message))
    if message.get_label() in self._messages:
      return False
    self._messages[message.get_label()] = message
    return True

  def get_supported_messages(self):
    """Returns list of supported messages.

    :returns: A list of :class:`Message` instances.
    """
    return self._messages.values()

  def unregister_message(self, message):
    """Unregisters message.

    :param message: A :class:`Message` instance.
    """
    if not isinstance(message, Message):
      raise TypeError('message has to be derived from class Message.')
    if message.label not in self._messages:
      return
    del self._messages[message.label]

  def get_name_format(self):
    """Returns desired name format.

    :returns: A string that represents name format.
    """
    return self._name_format

  def set_name_format(self, frmt):
    if not typecheck.is_string(frmt):
      raise TypeError('Name format must be string')
    self._name_format = frmt

  def set_runner(self, runner):
    if not typecheck.is_string(runner):
      raise TypeError("Runner must be string: %s" % runner)
    self._runner = runner

  def get_runner(self):
    """Returns runner's name."""
    return self._runner

  def set_name(self, name):
    if not name:
      raise TypeError('Name cannot be None value')
    if not typecheck.is_string(name):
      raise TypeError('Must be string')
    self._name = name

  def get_name(self):
    """Returns thread name."""
    return self._name

  def has_port(self):
    """Returns whether or not this thread has a port for communication.

    :returns: `True` or `False`.
    """
    return not self.get_port() is None

  def set_port(self, port):
    if not port or not isinstance(port, Port):
      raise TypeError("Port must be derived from bb.app.os.port.Port: %s" %
                      port)
    if self.has_port():
      self.remove_port()
    self._port = port
    if not port.get_name():
      port.set_name(port.name_format % self.get_name())
    return self

  def remove_port(self):
    self._port = None

  def get_port(self):
    """Returns port used by this thread for communication purposes."""
    return self._port

  def __str__(self):
    return "%s[name=%s,runner=%s,has_port=%s]" % (self.__class__.__name__,
                                                 self.get_name(),
                                                 self.get_runner(),
                                                 self.has_port())

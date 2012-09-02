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

"""The following example shows the most simple case how to define a new message
handler by using :func:`Messenger.message_handler` decorator::

  serial_open_msg = Message('SERIAL_OPEN', ('rx', 'tx'))
  serial_messenger = Messenger('SERIAL_MESSENGER')
                   .add_message_handler(serial_open_msg,  'serial_open_handler')

Or the same example, but as a class::

  class SerialMessenger(Messenger):
    NAME = 'SERIAL_MESSENGER'
    MESSAGE_HANDLERS = {
      Message('SERIAL_OPEN', ('rx', 'tx')): 'serial_open_handler',
    }

  When a :class:`SerialMessenger` object receives a ``SERIAL_OPEN`` message,
  the message is directed to :func:`SerialMessenger.serial_open_handler`
  handler for the actual processing.
"""

import logging

from bb.os.thread import Thread
from bb.lib.utils import typecheck

class Argument(str):
  def __init__(self, string):
    str.__init__(self, string)
    self._type = None

  @property
  def type(self):
    return self._type

  @type.setter
  def type(self, type):
    self._type = type

class Message(object):
  """This class describes message structure passed between threads for
  communication purposes.
  """

  def __init__(self, id, arguments):
    self._id = None
    self._arguments = []
    if id:
      self.id = id
    if arguments:
      self.arguments = arguments

  @property
  def id(self):
    return self._id

  @id.setter
  def id(self, id):
    if not typecheck.is_string(id):
      raise TypeError('`id` has to be a string')
    self._id = id

  @property
  def arguments(self):
    return self._arguments

  @arguments.setter
  def arguments(self, args):
    self._arguments = []
    if not typecheck.is_sequence(args):
      raise TypeError('`args` has to be a sequence')
    for arg in args:
      if not isinstance(arg, Argument):
        arg = Argument(arg)
      self._arguments.append(arg)

class Messenger(Thread):
  """This class is a special form of thread, which allows to automatically
  provide an action for received message by using specified map of predefined
  handlers.

  .. note::

    In order to privent any conflicts with already defined methods the message
    handler should be named by concatinating `_handler` postfix to the the
    name of handler, e.g. ``serial_open_handler``.
  """

  MESSAGE_HANDLERS = {}

  def __init__(self, name=None, message_handlers={}):
    Thread.__init__(self, name)
    self._message_handlers = {}
    if hasattr(self, 'MESSAGE_HANDLERS'):
      for message, handler in self.MESSAGE_HANDLERS.items():
        self.add_message_handler(message, handler)
    if message_handlers:
      self.add_message_handlers(message_handlers)

  def get_message_handler(self, message):
    if not typecheck.is_string(message):
      raise TypeError('message has to be a string')
    return self._message_handlers.get(message, None)

  def get_supported_commands(self):
    """Return list of supported commands."""
    return self._message_handlers.keys()

  def add_message_handler(self, message, handler):
    """Maps a command extracted from a message to the specified handler
    function. Note, handler's name should ends with '_handler'.
    """
    if not typecheck.is_string(message) or not typecheck.is_string(handler):
      raise TypeError('message and handler both have to be strings')
    if not handler.endswith('_handler'):
      logging.warning("WARNING: Message handler '%s' that handles message '%s' "
                      "doesn't end with '_handler'" % (handler, message))
    self._message_handlers[message] = handler
    return self

  def add_message_handlers(self, message_handlers):
    if not typecheck.is_dict(message_handlers):
      raise TypeError('message_handlers has to be a dict')
    for message, handler in message_handlers.items():
      self.add_message_handler(message, handler)
    return self

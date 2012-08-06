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

class Messenger(bb.Thread):
  """This class is a special form of thread, which allows to automatically
  provide an action for received message by using specified map of predefined
  handlers.

  The following example shows the most simple case how to define a new message
  handler by using :func:`Messenger.message_handler` decorator::

    my_messenger = Messenger('MY_MESSENGER')
                   .add_message_handler('SERIAL_OPEN', 'serial_open_handler')

  Or the same example, but as a class::

    class SerialMessenger(Messenger):
      NAME = 'MY_MESSENGER'
      MESSAGE_HANDLERS = {'SERIAL_OPEN': 'serial_open_handler'}

  When a :class:`SerialMessenger` object receives a ``SERIAL_OPEN`` message,
  the message is directed to :func:`SerialMessenger.serial_open_handler`
  handler for the actual processing.

  .. note::

    In order to privent any conflicts with already defined methods the message
    handler should be named by concatinating `_handler` postfix to the the
    name of handler, e.g. ``serial_open_handler``.
  """

  MESSAGE_HANDLERS = {}

  def __init__(self, name, message_handlers={}):
    if not typecheck.is_string(name):
      raise TypeError('Messengers name has to be a string')
    bb.Thread.__init__(name)
    self._message_handlers = {}
    if message_handlers:
      self.add_message_handlers(message_handlers)

  def get_message_handler(self, message):
    if not typecheck.is_string(message):
      raise TypeError('message has to be a string')
    return self._message_handlers.get(message, None)

  def add_message_handler(self, message, handler):
    """Maps a command extracted from a message to the specified handler
    function. Note, handler's name should ends with '_handler'.
    """
    if not typecheck.is_string(message) or not typecheck.is_string(handler):
      raise TypeError('message and handler both have to be strings')
    if not handler.endswith('_handler'):
      print "WARNING: Message handler '%s' that handles message '%s' " \
          "doesn't end with '_handler'" % (handler, message)
    self._message_handlers[message] = handler
    return self

  def add_message_handlers(self, message_handlers):
    if not typecheck.is_dict(message_handlers):
      raise TypeError('message_handlers has to be a dict')
    for message, handler in message_handlers.items():
      self.add_message_handler(message, handler)
    return self
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
#
# Author: Oleksandr Sviridenko

"""The *messenger* is ITC wrapper that hides message routing. The
:class:`Messenger` processes message sent by other threads and also sends
messages to other threads. To communicate with other threads it uses BBOS native
ITC mechanism.

The following example shows how to create simple messenger
:class:`MyMessenger`::

  class MyMessenger(Messenger):
    message_handlers = [
      ('open',  ('MY_MSNGR_OPEN', [('pin', 2)]),
                ('MY_MSNGR_OPEN_STATUS', [('pin', 2), ('status', 1)]))
      ('close', ('MY_MSNGR_CLOSE', [('pin', 2)])
                ('MY_MSNGR_CLOSE_STATUS', [('pin', 2), ('status', 1)]))
    ]

  my_msngr = MyMessenger()

When a :class:`MyMessenger` object receives a ``MY_MSNGR_OPEN`` message, the
message is directed to ``open`` handler for the actual processing.
"""

from bb.utils import logging
from bb.utils import typecheck
from bb.app.os.thread import Thread
from bb.app.os.message import Message

logger = logging.get_logger("bb")

class MessageHandler(object):
  """This class represents handler that provides a description to BBOS of how to
  handle specific message, i.e. it tells to messenger how to handle received
  message or *target message* and to send *response message* if required.

  :param name: A string that represents handler's name.
  :param target_message: A :class:`~bb.app.os.message.Message` instance that
    messenger is going to receive.
  :param response_message: A :class:`~bb.app.os.message.Message` instance that
    messenger has to send back as response to `target_message`.
  """

  def __init__(self, name, target_message, response_message=None):
    self._name = None
    self._set_name(name)
    self._target_message = target_message
    self._response_message = response_message

  def __str__(self):
    return "%s[name='%s', target_message=%s]" \
        % (self.__class__.__name__, self._name,
           self._target_message)

  def _set_name(self, name):
    if not typecheck.is_string(name):
      raise TypeError()
    self._name = name

  def get_name(self):
    """Returns a string that represents handler's name."""
    return self._name

  def get_target_message(self):
    """Returns target message.

    :returns: A :class:`Message` instance.
    """
    return self._target_message

  def get_response_message(self):
    """Returns response message.

    :returns: A :class:`Message` instance.
    """
    return self._response_message

class Messenger(Thread):
  """This class is a special form of thread, which allows to automatically
  provide an action for received message by using specified map of predefined
  handlers.

  .. note::

    In order to privent any conflicts with already defined methods the message
    handler should be named by concatinating `_handler` postfix to the the
    name of handler, e.g. ``serial_open_handler``.

  :param name: A string that represents messenger's name.
  :param idle_action: A string that represents function name that will be called
    when messenger is idle.
  :param default_action: A string that represents function name that will be
    called to handle unknown message.
  :param port: A :class:`Port` instance that will keep messages for the messenger.
  """

  message_handlers = []
  idle_action = None
  default_action = None

  def __init__(self, name=None, runner=None, message_handlers=[],
               idle_action=None, default_action=None, port=None):
    Thread.__init__(self, name, runner=runner, port=port)
    self._default_action = None
    self._idle_action = None
    self._message_handlers = {}
    if default_action or getattr(self.__class__, "default_action", None):
      self.set_default_action(default_action or self.__class__.default_action)
    if idle_action or getattr(self.__class__, "idle_action", None):
      self.set_idle_action(idle_action or self.__class__.idle_action)
    if message_handlers or getattr(self.__class__, "message_handlers", None):
      self.add_message_handlers(message_handlers \
                                  or self.__class__.message_handlers)

  def get_default_action(self):
    return self._default_action

  def set_default_action(self, action):
    if not typecheck.is_function(action):
      raise TypeError("action has to be a function: %s" % action)
    self._default_action = action

  def get_idle_action(self):
    """Returns a string that represents idle function name."""
    return self._idle_action

  def set_idle_action(self, action):
    if not typecheck.is_function(action):
      raise TypeError("action has to be a function: %s" % action)
    self._idle_action = action

  def get_message_handlers(self):
    """Returns all registered message handlers.

    :returns: A list of :class:`MessageHandler` instances.
    """
    return self._message_handlers.values()

  def get_messages(self):
    """Returns a list of unique messages supported by this messenger.

    :returns: A list of :class:`Message` instances.
    """
    messages = []
    for handler in self.get_message_handlers():
      messages.extend([handler.get_target_message(),
                       handler.get_response_message()])
    return messages

  def add_message_handler(self, handler):
    """Maps a command extracted from a message to the specified handler
    function. Note, handler's name should ends with `_handler`.

    :param handler: A :class:`MessageHandler` instance.
    """
    if not isinstance(handler, MessageHandler):
      raise TypeError('message handler has to be derived from MessageHandler')
    for message in (handler.get_target_message(), handler.get_response_message()):
      if message and not self.register_message(message):
        return self
    # TODO: do we need this warning?
    #if not handler.get_name().endswith('_handler'):
    #  logger.warning("Message handler %s that handles message %s "
    #                 "doesn't end with '_handler'"
    #                 % (handler.get_name(), message))
    self._message_handlers[handler.get_target_message()] = handler
    return self

  def add_message_handlers(self, message_handlers):
    """Add message handlers.

    :param message_handlers: A list/tuple of :class:`MessageHandler`.
    """
    if not typecheck.is_list(message_handlers):
      raise TypeError('message_handlers has to be a list')
    for handler in message_handlers:
      if isinstance(handler, MessageHandler):
        self.add_message_handler(handler)
      else:
        if not typecheck.is_tuple(handler):
          raise TypeError("handler must be a tuple: %s" % type(handler))
        if len(handler) < 2:
          raise Exception("Handler should have more than two parameters")
        handler = list(handler)
        if typecheck.is_tuple(handler[1]):
          handler[1] = Message(*handler[1])
        else:
          raise TypeError()
        if len(handler) > 2:
          if typecheck.is_tuple(handler[2]):
            handler[2] = Message(*handler[2])
          else:
            raise TypeError()
        handler = MessageHandler(*handler)
      self.add_message_handler(handler)
    return self

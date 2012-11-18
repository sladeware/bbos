#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

"""
Example:

    from bb.os import Thread, Messenger, Channel

    sender = Thread("SENDER", "sender_runner")
    receiver = Messenger("RECEIVER", "receiver_runner",
                         channels=(Channel((Message("PING"),
                                            Message("PING", ("status"))))))
"""

from bb.os.message import Message

class Channel(object):

  def __init__(self, input_message, output_message):
    self._input_message = None
    self._output_message = None
    self.set_input_message(input_message)
    self.set_output_message(output_message)

  def set_input_message(self, message):
    self._input_message = message

  def get_input_message(self):
    return self._input_message

  def set_output_message(self, message):
    self._output_message = message

  def get_output_message(self):
    return self._output_message

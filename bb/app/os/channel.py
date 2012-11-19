#!/usr/bin/env python
#
# http://bionicbunny.org/
# Copyright (c) 2012 Sladeware LLC
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

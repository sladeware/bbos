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

from bb.utils.testing import unittest
from bb.app.os.messenger import Message, Messenger

class MessageTest(unittest.TestCase):

  def test_id(self):
    msg = Message("SERIAL_OPEN", ("rx", "tx"))
    self.assert_equal("SERIAL_OPEN", msg.get_label())

  def test_io_fields(self):
    msg = Message("SERIAL_OPEN", ("rx", "tx"))
    self.assert_equal(2, len(msg.get_fields()))
    for field in msg.get_fields():
      self.assert_true(isinstance(field, Message.field_type))
    for i, name, size in ((0, "rx", 0), (1, "tx", 0)):
      self.assert_equal(name, msg.get_fields()[i].name)
      self.assert_equal(size, msg.get_fields()[i].size)

class MessagingTest(unittest.TestCase):
  pass

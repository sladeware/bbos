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
from bb.testing import unittest

from bb.os.messenger import Message, Messenger, Argument

class MessageTest(unittest.TestCase):
  def setup(self):
    self._message = Message('SERIAL_OPEN', ('rx', 'tx'))

  def test_id(self):
    self.assert_equal(self._message.id, 'SERIAL_OPEN')

  def test_arguments(self):
    self.assert_equal(len(self._message.arguments), 2)
    for arg in self._message.arguments:
      self.assert_true(isinstance(arg, Argument))
      self.assert_is_none(arg.type)
    self.assert_equal(self._message.arguments[0], 'rx')
    self.assert_equal(self._message.arguments[1], 'tx')

class MessagingTest(unittest.TestCase):
  pass

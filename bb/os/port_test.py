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

import unittest

import bb
import bb.os as bbos

class PortTest(unittest.TestCase):
  def setUp(self):
    pass

  def testPortName(self):
    p1 = bbos.Port("P1", 1)
    self.assertEqual(p1.get_name(), "P1")

  def testPortCapacity(self):
    p1 = bbos.Port("P1", 1)
    self.assertEqual(p1.get_capacity(), 1)

if __name__ == '__main__':
  unittest.main()

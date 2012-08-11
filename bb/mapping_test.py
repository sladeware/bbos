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

class MappingTest(unittest.TestCase):
  def test_thread_registration(self):
    t1 = bb.os.Thread("T1")
    t2 = bb.os.Thread("T2")
    mapping = bb.Mapping("M1")
    mapping.register_threads([t1, t2])
    self.assertEqual(len(mapping.get_threads()), 2)

  def test_name(self):
    mapping = bb.Mapping("M1")
    self.assertEqual(mapping.get_name(), "M1")

if __name__ == '__main__':
    unittest.main()

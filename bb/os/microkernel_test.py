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

class MicrokernelTest(unittest.TestCase):
  def setUp(self):
    self._microkernel = bb.os.Microkernel()

  def testThreadRegistration(self):
    t1 = bb.Thread("T1")
    self._microkernel.register_thread(t1)
    self.assertEqual(self._microkernel.get_num_threads(), 1)
    self._microkernel.unregister_thread(t1)
    self.assertEqual(self._microkernel.get_num_threads(), 0)

if __name__ == '__main__':
  unittest.main()

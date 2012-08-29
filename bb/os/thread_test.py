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

import bb
import bb.os as bbos
from bb.testing import unittest

class ThreadTest(unittest.TestCase):
  def setup(self):
    pass

  def test_port_management(self):
    p0 = bbos.Port("P0", 1)
    p1 = bbos.Port("P1", 1)
    p2 = bbos.Port("P2", 1)
    ports = [p0, p1, p2]
    t0 = bbos.Thread("T0", ports=ports)
    self.assert_equal(t0.get_num_ports(), 3)
    t0.remove_all_ports()
    self.assert_equal(t0.get_num_ports(), 0)
    # Test default port
    for port in ports:
      t0.add_port(port)
    t0.add_port(p1, default=True)
    self.assert_equal(t0.get_default_port(), p1)

  def test_name(self):
    t0 = bbos.Thread("T0")
    self.assert_equal(t0.get_name(), "T0")

  def test_runner(self):
    t0 = bbos.Thread("T0", "old_hello_world")
    self.assert_equal(t0.get_runner(), "old_hello_world")
    t0.set_runner("new_hello_world")
    self.assert_equal(t0.get_runner(), "new_hello_world")

if __name__ == '__main__':
  unittest.main()

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

from bb.testing import unittest
from bb.hardware.devices.device import Device
from bb.hardware import primitives

class DeviceTest(unittest.TestCase):
  def setup(self):
    pass

  def test_add_elements(self):
    e1 = primitives.ElectronicPrimitive('P1')
    e2 = Device('D2')
    d = Device('D1')
    d.add_elements([e1, e2])
    self.assert_equal(len(d.get_elements()), 2)

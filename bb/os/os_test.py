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

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = 'Oleksandr Sviridenko'

import bb
from bb.hardware.devices.processors import PropellerP8X32A_Q44
from bb.testing import unittest

class OSTest(unittest.TestCase):
  def setup(self):
    self._processor = PropellerP8X32A_Q44()
    self._os = bb.os.OS(processor=self._processor)

  def test_get_kernels(self):
    self.assert_equal(self._os.get_kernels(), [])

if __name__ == '__main__':
  unittest.main()

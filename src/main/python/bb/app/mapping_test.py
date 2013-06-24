# http://www.bionicbunny.org/
# Copyright (c) 2013 Sladeware LLC
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

from bb.utils.testing import unittest
from bb.app.mapping import Mapping
from bb.app.os.thread import Thread

class MappingTest(unittest.TestCase):

  def test_thread_registration(self):
    m = Mapping('M1')
    m.register_threads([Thread('T1'), Thread('T2')])
    self.assert_equal(2, len(m.get_threads()))

  def test_name(self):
    m = Mapping('M1')
    self.assert_equal('M1', m.get_name())

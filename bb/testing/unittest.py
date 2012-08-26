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

from __future__ import absolute_import

__author__ = 'Oleksandr Sviridenko'

import unittest

class TestCase(unittest.TestCase):
  assert_equal = unittest.TestCase.assertEqual
  assert_is_not = unittest.TestCase.assertIsNot

  def setup(self):
    pass

  def setUp(self):
    return self.setup()

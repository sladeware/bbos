# -*- coding: utf-8; -*-
#
# Copyright (c) 2013 Sladeware LLC
# http://www.bionicbunny.org/
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

import unittest

TestLoader = unittest.TestLoader

TextTestRunner = unittest.TextTestRunner

class TestCase(unittest.TestCase):
  """This class represents the smallest testable units."""

  def __init__(self, *args, **kwargs):
    unittest.TestCase.__init__(self, *args, **kwargs)
    if hasattr(self, "setup"):
      self.setUp = self.setup
    if hasattr(self, "teardown"):
      self.tearDown = self.teardown

  assert_equal = unittest.TestCase.assertEqual
  assert_not_equal = unittest.TestCase.assertNotEqual
  assert_is_not = unittest.TestCase.assertIsNot
  assert_is_none = unittest.TestCase.assertIsNone
  assert_is_not_none = unittest.TestCase.assertIsNotNone
  assert_true = unittest.TestCase.assertTrue
  assert_false = unittest.TestCase.assertFalse
  assert_raises = unittest.TestCase.assertRaises

main = unittest.main

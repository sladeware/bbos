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
#
# Author: Oleksandr Sviridenko

from bb.app.hardware import primitives
from bb.utils.testing import unittest

class PrimitivesTest(unittest.TestCase):

  def test_primitive(self):
    p0 = primitives.Primitive("P0")
    self.assert_equal(p0.get_designator(), "P0")
    x0 = primitives.Primitive(designator_format="X%d")
    self.assert_equal(x0.get_designator(), "X0")

  def test_primitive_properties(self):
    p0 = primitives.Primitive()
    p0.properties["weight"] = 10
    self.assert_equal(len(p0.get_properties()), 1)
    self.assert_equal(p0.properties["weight"], 10)

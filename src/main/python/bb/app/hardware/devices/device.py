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

import networkx

from bb.app.hardware import primitives
from bb.app.os.drivers import Driver
from bb.utils import typecheck

class Sketch(object):
  G = networkx.Graph()

  def __init__(self):
    pass

class Device(primitives.ElectronicPrimitive):
  """Base device class for any kind of devices. It also keeps driver instance
  that manages this device for OS.
  """

  DRIVER_CLASS = None
  DESIGNATOR_FORMAT = "D%d"

  def __init__(self, designator=None, designator_format=None):
    primitives.ElectronicPrimitive.__init__(self, designator, designator_format)
    self._driver = None
    if self.DRIVER_CLASS:
      self._set_driver(self.DRIVER_CLASS())

  # TODO: temporary soluiton. Do we need to make it public?
  def _set_driver(self, driver):
    if not isinstance(driver, Driver):
      raise TypeError("'driver' must be derived from Driver.")
    self._driver = driver

  def get_driver(self):
    return self._driver

  @property
  def G(self):
    return self._g

  def is_connected_to(self, element):
    return Sketch.G.has_edge(self, element)

  def add_elements(self, elements):
    for element in elements:
      self.add_element(element)
    return self

  def add_element(self, element):
    if not isinstance(element, primitives.ElectronicPrimitive):
      raise TypeError("Must be derived from primitives.ElectronicPrimitive")
    self.connect_to(element)
    return element

  def update_element(self, original, new):
    original_designator = original.get_designator()
    self.remove_element(original)
    new.set_designator(original_designator)
    self.add_element(new)

  def remove_element(self, element):
    pass

  def get_elements(self):
    return Sketch.G.neighbors(self)

  def find_element(self, by):
    # TODO: this method has to be modified! Add very basic design.
    if typecheck.is_string(by):
      for element in self.get_elements():
        if element.get_designator() == by:
          return element
    return None

  def find_elements(self, by):
    return []

  def connect_to(self, element):
    Sketch.G.add_edge(self, element)

  def disconnect_elements(self, src, dest):
    pass

  def clone(self):
    """Clone this device instance."""
    clone = primitives.ElectronicPrimitive.clone(self)
    for origin_pin in self.find_elements(primitives.Pin):
      pin = origin_pin.clone()
      clone.add_element(pin)
    return clone

  def __str__(self):
    return "%s[designator=%s]" % (self.__class__.__name__,
                                  self.get_designator())

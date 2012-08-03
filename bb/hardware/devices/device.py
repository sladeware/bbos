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

import networkx

from bb.hardware import primitives
from bb.lib.utils import typecheck

class Sketch(object):
  G = networkx.Graph()

  def __init__(self):
    pass

class Sketch(object):
  G = networkx.Graph()

  def __init__(self):
    pass

class Device(primitives.ElectronicPrimitive):
  DRIVER_CLASS=None
  DESIGNATOR_FORMAT="D%d"

  def __init__(self, designator=None, designator_format=None):
    primitives.ElectronicPrimitive.__init__(self, designator,
                                            designator_format)

  @property
  def G(self):
    return self._g

  def is_connected_to_element(self, element):
    return Sketch.G.has_edge(self, element)

  def add_elements(self, elements):
    for element in elements:
      self.add_element(element)
    return self

  def add_element(self, element):
<<<<<<< HEAD
    if not isinstance(element, primitives.ElectronicPrimitive):
      raise TypeError('Must be primitives.ElectronicPrimitive')
=======
>>>>>>> upstream/master
    self.connect_to(element)
    return self

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
<<<<<<< HEAD
    # TODO: this method has to be modified! Add very basic design.
    if typecheck.is_string(by):
      for element in self.get_elements():
        if element.get_designator() == by:
          return element
    return None
=======
    pass
>>>>>>> upstream/master

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
    return "Device <%s>" % self.get_designator()

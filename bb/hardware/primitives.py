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

"""This module contains basic hardware primitives, such as pin, bus, wire,
etc. and other hardware primitives such as notes.
"""

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'
__author__ = 'Oleksandr Sviridenko'

import bb
from bb.utils import typecheck

__all__ = ['Primitive', 'ElectronicPrimitive', 'Pin', 'Wire', 'Bus', 'Note']

class Primitive(bb.Object):
  """This class is basic for any primitive.

  Each primitive has unique ID -- designator for identification that can be
  obtained by :func:`get_designator`. However this ID is unique only within
  primitives from the same device. By default the system tries to generate
  designator with help of :func:`get_designator_format()` and
  :func:`generate_designator`. However it can be changed manually by using
  :func:`set_designator` method.

  A primitive may also have properties where each property is represented by
  :class:`Primitive.Property`. For example, if you would like to add weight of
  your primitive ``my_primitive``, you can do this as follows::

    my_primitive.add_property(Primitive.Property("weight", 87))

  Now people will be able to define the weight of the primitive::

    print my_primitive.get_primitive("weight").value
  """

  DESIGNATOR_FORMAT="P%d"
  """This designator format will be used by all the primitives that will inherit
  this class. By default primitives will have such designators: ``P0``, ``P1``,
  ..., etc. The format can be changed later by using
  :func:`set_designator_format` method.
  """

  PROPERTIES = ()
  """Dictionary of default properties used by all the primitives that will
  inherit this class.
  """

  class Property(object):
    """This class represents property of a primitive. Each property consists of
    `name` and `value`.
    """
    def __init__(self, name, value=None):
      self._name = name
      self._value = value

    @property
    def name(self):
      return self._name

    @property
    def value(self):
      return self._value

    @value.setter
    def value(self, new_value):
      self._value = new_value

  def __init__(self, designator=None, designator_format=None):
    bb.Object.__init__(self)
    self._properties = dict()
    self._id = id(self)
    self._designator_format = None
    self._designator = None
    if designator_format:
      self.set_designator_format(designator_format)
    else:
      self.set_designator_format(self.DESIGNATOR_FORMAT)
    if designator:
      self.set_designator(designator)
    else:
      self.generate_designator()
    if self.PROPERTIES:
      self.add_properties(self.PROPERTIES)

  def clone(self):
    """Creates and returns a copy of this object. The default implementation
    returns a so-called "shallow" copy: It creates a new instance of the same
    class and then copies the field values (including object references) from
    this instance to the new instance. A "deep" copy, in contrast, would also
    recursively clone nested objects.
    """
    clone = self.__class__()
    for k, v in self.__dict__.iteritems():
      setattr(clone, k, v)
    return clone

  def get_designator_format(self):
    """Defines the format string to be used with the part designator. A
    reference designator unambiguously identifies a component in an electrical
    schematic (circuit diagram) or on a printed circuit board (PCB). The
    reference designator usually consists of one or two letters followed by a
    number, e.g. R13, C1002.
    """
    return self._designator_format

  def generate_designator(self, counter=0):
    """Generate a new designator and set it as the current one by using
    :func:`set_designator`. Return new designator. Usually generator uses
    designator format and `counter` that represents the number of relatives.
    """
    designator = self.get_designator_format() % counter
    self.set_designator(designator)
    return designator

  def set_designator_format(self, frmt):
    self._designator_format = frmt

  def get_designator(self):
    """Return designator value.

    Designator is the name of a part on a printed circuit by
    convention beginning with one or two letters followed by a
    numeric value. The letter designates the class of component;
    eg. "Q" is commonly used as a prefix for transistors.

    It is very important to clearly understand the importance of
    the reference designator and the rules for assigning reference
    designators. An alphanumeric reference designator is used to
    uniquely identify each part. A given circuit might have ten
    1.0k resistors used in different locations. Each of these
    resistors is given a unique reference designator, for example,
    Rl, R5, and R7. In addition to the schematic, the reference
    designators also appear on the PCB legend silkscreen, assembly
    drawing, and bill of materials. Manufacturing uses the
    reference designators to determine where to stuff parts on the
    board. Field service uses them to identify and replace failed
    parts.

    See also :func:`generate_designator`.
    """
    return self._designator

  def set_designator(self, text):
    # TODO(team): designator should be unique within its graph
    self._designator = text
    return self

  def get_id(self):
    return self._id

  def set_id(self, value):
    self._id = value

  def add_properties(self, properties):
    if not typecheck.is_sequence(properties):
      raise TypeError("Has to be list")
    for property in properties:
      self.add_property(property)

  def add_property(self, property):
    """Add a new property for the primitive."""
    if not isinstance(property, Primitive.Property):
      raise Exception("Not a Property")
    self._properties[property.name] = property

  def has_property(self, property_):
    """Return whether or not the primitive has a property `property_`. The
    `property_` can be defined as a string or instance of :class:`Property`
    class.
    """
    property_name = property_
    if isinstance(property_, Primitive.Property):
      property_name = property_.name
    return property_name in self._properties

  def set_property(self, name, value):
    property_ = self.get_property(name)
    if property_:
      property_.value = value
      return property_
    property_ = Primitive.Property(name, value)
    self.add_property(property_)
    return property_

  def get_properties(self):
    return self._properties.values()

  def get_property(self, name):
    if not self.has_property(name):
      return None
    return self._properties[name]

  def get_property_value(self, name, default=None):
    property_ = self.get_property(name)
    if not property_:
      return default
    return self.get_property(name).value

  def __str__(self):
    """Returns a string containing a concise, human-readable
    description of this object.
    """
    return "Primitive <%s>" % self.get_designator()

class ElectronicPrimitive(Primitive):
  """This class represents basic electrical design primitive."""

  def __init__(self, designator=None, designator_format=None):
    Primitive.__init__(self, designator, designator_format)

class Pin(ElectronicPrimitive):
  """A pin is an electrical design primitive derived from
  :class:`ElectronicPrimitive` class. Pins give a part its electrical properties
  and define connection points on the part for directing signals in and out.

  Each pin has electrical type. Electrical type represents the type of
  electrical connection the pin makes. This can be used to detect electrical
  wiring errors in your schematic.
  """

  # Possible electrical types.
  INPUT_TYPE = 0
  IO_TYPE = 1
  OUTPUT_TYPE = 2

  def __init__(self):
    ElectronicPrimitive.__init__(self)
    self._connections = dict()
    self._electrical_type = None

  def get_electrical_type(self):
    """Return electrical type of this pin."""
    return self._electrical_type

  def set_electrical_type(self, type_):
    """Set electrical type. See :class:`Pin.ElectricalTypes` to find support
    types.
    """
    if not getattr(Pin.ElectricalTypes, type_):
      raise
    self._electrical_type = type_

  def connect_to(self, pin):
    """Connect source pin to destination pin."""
    if not isinstance(pin, Pin):
      raise Exception("'%s' must be a Pin" % pin)
    G.add_edge(self, pin)
    G.add_edge(pin, self)
    if not self.is_connected_to(pin):
      self.__connections[id(pin)] = pin
      pin.connect_to(self)

  def is_connected_to(self, pin):
    return id(pin) in self.__connections

class Wire(ElectronicPrimitive):
  """A wire is an electrical design primitive derived from
  :class:`ElectronicPrimitive`. It is an object that forms an electrical
  connection between points on a schematic and is analogous to a physical
  wire.

  The pins can be set separately.
  """

  def __init__(self):
    ElectronicPrimitive.__init__(self)
    self._first_pin = None
    self._second_pin = None

  def connect(self, first_pin, second_pin):
    """Connect two pins."""
    self.set_first_pin(first_pin)
    self.set_second_pin(second_pin)
    G.add_edge(first_pin, second_pin)
    G.add_edge(second_pin, first_pin)

  def find_pin(self, by):
    for pin in (self._first_pin, self._second_pin):
      if pin.get_designator() == by:
        return pin

  def disconnect(self):
    self._first_pin = self._second_pin = None

  def set_first_pin(self, pin):
    self._first_pin = pin

  def get_first_pin(self):
    return self._first_pin

  def set_second_pin(self, pin):
    self._second_pin = pin

  def get_second_pin(self):
    return self._second_pin

  def clone(self):
    """Clone this wire. Return cloned :class:`Wire` object."""
    clone = ElectronicPrimitive.clone(self)
    # Clone first pin if possible
    if self.get_first_pin():
      clone.set_first_pin(self.get_first_pin().clone())
    if self.get_second_pin():
      clone.set_second_pin(self.get_second_pin().clone())
    if not None in (clone.get_first_pin(), clone.get_second_pin()):
      clone.connect(clone.get_first_pin(), clone.get_second_pin())
    # if not None in (self.get_first_pin(), self.get_second_pin()):
    #   clone.connect(self.get_first_pin().clone(), self.get_second_pin().clone())
    return clone

class Note(Primitive):
  """A note is a design primitive (non-electrical), derived from class
  :class:`Primitive`. It is used to add informational or instructional text to a
  specific area within a schematic, in a similar vain to that of commenting a
  program's source code. Mostly used by GUI.
  """
  def __init__(self):
    Primitive.__init__(self)
    self._text = ""

  @property
  def text(self):
    return self._text

  @text.setter
  def text(self, text):
    self._text = text

class Bus(ElectronicPrimitive):
  """A bus is an electrical design primitive. It is an object that represents
  a multi-wire connection.
  """

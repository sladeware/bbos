#!/usr/bin/env python

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

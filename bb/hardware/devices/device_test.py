#!/usr/bin/env python

import unittest

from bb.hardware.devices.device import Device
from bb.hardware import primitives

class DeviceTest(unittest.TestCase):
    def setUp(self):
        pass

    def testAddElements(self):
        e1 = primitives.ElectronicPrimitive("P1")
        e2 = Device("D2")
        d = Device("D1")
        d.add_elements([e1, e2])
        self.assertEqual(len(d.get_elements()), 2)

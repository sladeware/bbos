#!/usr/bin/env python

import unittest

from bb.hardware import primitives

class PrimitivesTest(unittest.TestCase):

    def testPrimitive(self):
        p0 = primitives.Primitive("P0")
        self.assertEqual(p0.get_designator(), "P0")
        x0 = primitives.Primitive(designator_format="X%d")
        self.assertEqual(x0.get_designator(), "X0")

    def testPrimitiveProperties(self):
        p0 = primitives.Primitive()
        p0.set_property("weight", 10)
        self.assertEqual(len(p0.get_properties()), 1)
        self.assertEqual(p0.get_property("weight").value, 10)

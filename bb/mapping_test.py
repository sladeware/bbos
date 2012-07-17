#!/usr/bin/env python

import unittest

import bb

class MappingTest(unittest.TestCase):
    def testThreadRegistration(self):
        t1 = bb.Thread("T1")
        t2 = bb.Thread("T2")
        mapping = bb.Mapping("M1")
        mapping.register_threads([t1, t2])
        self.assertEqual(len(mapping.get_threads()), 2)

    def testNaming(self):
        mapping = bb.Mapping("M1")
        self.assertEqual(mapping.get_name(), "M1")

if __name__ == '__main__':
    unittest.main()

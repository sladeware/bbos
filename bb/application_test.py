#!/usr/bin/env python

import unittest

import bb

class ApplicationTest(unittest.TestCase):
    def testMappingRegistration(self):
        app = bb.Application()
        m1 = bb.Mapping("M1")
        m2 = bb.Mapping("M2")
        app.register_mappings([m1, m2])
        self.assertEqual(app.get_num_mappings(), 2)

if __name__ == '__main__':
    unittest.main()

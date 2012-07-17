#!/usr/bin/env python

import unittest

import bb

class OSTest(unittest.TestCase):
    def setUp(self):
        self._os = bb.os.OS()

    def testMicrokernel(self):
        self.assertIsNot(self._os.get_microkernel(), None)

if __name__ == '__main__':
    unittest.main()

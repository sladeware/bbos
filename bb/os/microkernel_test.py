#!/usr/bin/env python

import unittest

import bb

class MicrokernelTest(unittest.TestCase):
    def setUp(self):
        self._microkernel = bb.os.Microkernel()

    def testThreadRegistration(self):
        t1 = bb.Thread("T1")
        self._microkernel.register_thread(t1)
        self.assertEqual(self._microkernel.get_num_threads(), 1)
        self._microkernel.unregister_thread(t1)
        self.assertEqual(self._microkernel.get_num_threads(), 0)

if __name__ == '__main__':
    unittest.main()

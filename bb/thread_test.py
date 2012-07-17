#!/usr/bin/env python

import unittest

from bb import Thread

class ThreadTest(unittest.TestCase):
    def setUp(self):
        pass

    def testThreadName(self):
        t1 = Thread("T1")
        self.assertEqual(t1.get_name(), "T1")

    def testThreadRunner(self):
        t1 = Thread("T1", "old_hello_world")
        self.assertEqual(t1.get_runner(), "old_hello_world")
        t1.set_runner("new_hello_world")
        self.assertEqual(t1.get_runner(), "new_hello_world")

if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python

import unittest
import unittest2
import sys

def main(test_path):
    suite = unittest2.loader.TestLoader().discover(test_path, "*_test.py")
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    main('/home/d2rk/Desktop/bionicbunny/bb')

#!/usr/bin/env python

import os
import sys
import unittest
import unittest2

def main(test_path):
  suite = unittest2.loader.TestLoader().discover(test_path, "*_test.py")
  unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
  root_dir_path = os.path.dirname(os.path.realpath(__file__))
  main(root_dir_path)
  sys.exit(0)

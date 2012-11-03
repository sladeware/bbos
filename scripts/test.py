#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

import os
import sys
import unittest
#import unittest2

TEST_FILE_SUFFIX = "*_test.py"
VERBOSITY = 2

def main(test_path):
  suite = unittest.TestLoader().discover(test_path, TEST_FILE_SUFFIX)
  unittest.TextTestRunner(verbosity=VERBOSITY).run(suite)
  return 0

if __name__ == "__main__":
  scripts_dir_path = os.path.dirname(os.path.realpath(__file__))
  bb_dir_path = os.path.join(scripts_dir_path, "..", "bb")
  sys.exit(main(bb_dir_path))

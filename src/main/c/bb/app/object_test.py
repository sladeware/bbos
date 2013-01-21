#!/usr/bin/env python

import bb
from bb.application.object import Object
from bb.testing import unittest

class ObjectTest(unittest.TestCase):

  def test_builder(self):
    obj = Object()
    bldr = bb.get_bldr(obj)
    self.assert_is_not_none(bldr)

if __name__ == "__main__":
  unittest.main()
  exit(0)

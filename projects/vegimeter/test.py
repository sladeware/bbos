#!/usr/bin/env python

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'

import bb
from bb.testing import unittest

import vegimeter

class VegimeterTest(unittest.TestCase):
  def setup(self):
    self.vegimeter = bb.application.get_mapping('Vegimeter')

  def test_mapping(self):
    self.assert_is_not_none(self.vegimeter)

  def test_ui_thread(self):
    ui = self.vegimeter.get_thread('UI')
    self.assert_is_not_none(ui)

  def test_control_panel(self):
    control_panel = self.vegimeter.get_thread('CONTROL_PANEL')
    self.assert_is_not_none(control_panel)

if __name__ == '__main__':
  unittest.main()

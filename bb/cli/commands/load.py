#!/usr/bin/env python

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'

import bb
from bb.cli.commands.command import Command

class load(Command):
  USAGE = '%prog load'
  SHORT_DESC = 'Load a binary'
  USES_BASEPATH = False

  def function(self):
    pass

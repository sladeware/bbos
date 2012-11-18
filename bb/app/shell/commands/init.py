#!/usr/bin/env python

from bb.shell.commands.command import Command

class init(Command):
  USAGE = '%prog init'
  SHORT_DESC = 'Init new application'
  USES_BASEPATH = False

  def function(self):
    pass

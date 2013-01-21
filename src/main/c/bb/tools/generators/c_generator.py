#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

from bb.tools.generators.generator import Generator

class CGenerator(Generator):

  def header(self, data, level=1):
    if level == 1:
      self.writeln("/" + "*" * 79)
      for line in data.split("\n"):
        self.writeln(" * " + line)
      self.writeln(" " + "*" * 78 + "/")
      self.writeln()
    elif level == 2:
      self.writeln("/" * 80)
      for line in data.split("\n"):
        self.comment(line)

  def comment(self, comment):
    lines = comment.split("\n")
    for line in lines:
      self.writeln("// " + line)

  def define(self, name, value):
    self.writeln("#define %s %s" % (name, value))

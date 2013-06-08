# http://www.bionicbunny.org/
# Copyright (c) 2013 Sladeware LLC
#
# Author: Oleksandr Sviridenko

from bb.tools.b3.buildfile import Rule

class Fileset(Rule, Rule.WithSources):

  def __init__(self, target=None, name=None, srcs=[], deps=[]):
    Rule.__init__(self, target, name, deps=deps)
    Rule.WithSources.__init__(self, srcs=srcs)

  def execute(self):
    pass

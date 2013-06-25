# -*- coding: utf-8; -*-
#
# http://www.bionicbunny.org/
# Copyright (c) 2013 Sladeware LLC
#
# Author: Oleksandr Sviridenko

from bb.tools.b3.buildfile import Rule

class Binary(Rule, Rule.WithSources):

  def __init__(self, target=None, name=None, srcs=[], deps=[],
               compiler_class=None):
    Rule.__init__(self, target, name, deps=deps)
    Rule.WithSources.__init__(self, srcs=srcs)
    self.compiler = None
    if compiler_class:
      self.compiler = compiler_class()

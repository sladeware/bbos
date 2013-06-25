# -*- coding: utf-8; -*-
#
# http://www.bionicbunny.org/
# Copyright (c) 2013 Sladeware LLC
#
# Author: Oleksandr Sviridenko

from bb.tools.b3.buildfile import Rule

class Library(Rule, Rule.WithSources):
  """The base class for library rules such as cc_library, java_library."""

  is_language_dependent = True
  abstract = True

  def __init__(self, target=None, name=None, srcs=[], deps=[]):
    Rule.__init__(self, target=target, name=name, deps=deps)
    Rule.WithSources.__init__(self, srcs=srcs)

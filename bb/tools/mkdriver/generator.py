#!/usr/bin/env python


class DriverGenerator(object):
  def __init__(self):
    self.__lang = None

  def gen(self):
    self.gen_driver()

  def gen_driver(self):
    raise NotImplemented()

  def get_language(self):
    return self.__lang

  def validate_target(self, target):
    if self.lang != target.get_language():
      raise Exception("Target %s requires %s based code-generator" % (target,
        target.get_language()))

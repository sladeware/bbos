#!/usr/bin/env python

class Image(object):

  def __init__(self):
    self._targets = []

  def add_target(self, target):
    self._targets.append(target)

  def add_targets(self, targets):
    for target in targets:
      self.add_target(target)

  def get_targets(self):
    return self._targets

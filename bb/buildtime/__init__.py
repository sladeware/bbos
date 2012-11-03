#!/usr/bin/env python

import inspect
import sys

import bb
from bb.object_build import Target

TARGETS = {}

def target_factory(name):
  def __init__(self):
    Target.__init__(self, self.BUILD_CASES)
  klass = type("%sTarget" % name, (Target,), {'__init__':__init__,})
  return klass

def get_target(obj):
  if not bb.is_build_time_stage():
    return None
  if inspect.isclass(obj):
    if issubclass(obj, Target):
      return obj
    target_class = target_factory(obj.__name__)
    TARGETS[obj] = target_class
    return target_class
  elif isinstance(obj, bb.Object):
    if not obj in TARGETS:
      target_class = get_target(obj.__class__)
      target = target_class()
      TARGETS[obj] = target_class
    return TARGETS[obj]
  return None

#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = 'Oleksandr Sviridenko'

from types import *

class Loader(object):
  """Abstract base class to define the interface that must be implemented by
  real loader classes.
  """

  DEFAULT_EXECUTABLES = dict()

  def __init__(self, verbose=False):
    self.verbose = verbose

  def load(self, *arg_list, **arg_dict):
    print "Loading"
    self._load(*arg_list, **arg_dict)

  def _load(self, *arg_list, **arg_dict):
    raise NotImplemented

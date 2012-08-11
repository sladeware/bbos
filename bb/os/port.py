#!/usr/bin/env python

# TODO(team): on this moment the name and capacity of the port cannot be changed
# in build-time and runtime respectively. However, I do not see a problem to
# allow developer to change this attributes in build-time.

class Port(object):
  """Thread communication technique. At some point, this is just a protected
  messaging pool for communication between threads.

  Each port has a ``name`` and ``capacity``, or how many messages it can keep.
  """

  def __init__(self, name, capacity):
    assert capacity > 0, "Port capacity must be greater than zero"
    self._name = name
    self._capacity = capacity

  def get_name(self):
    return self._name

  def get_capacity(self):
    return self._capacity

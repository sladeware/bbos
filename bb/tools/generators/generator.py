#!/usr/bin/env python

import bb

class Generator(object):

  def __init__(self, filename=None):
    self._fname = None
    self._fh = None
    if filename:
      self.open(filename)

  def create(self, filename):
    self._fh = open(filename, 'w')
    self.write_header(
      'WARNING: this file was automatically generated.\n'
      'Do not edit it by hand unless you know what you\'re doing.'
      )
    return self

  def write_header(self, data, level=1):
    pass

  def write(self, data):
    self._fh.write(data)

  def writeln(self, data=''):
    self._fh.write(data + "\n")

  def edit(self, filename):
    self.open(filename)
    self.write_header('Edits', 2)
    return self

  def open(self, filename, mode='a'):
    """If file is not exist, it will be created. See create()."""
    self._fname = filename
    if not bb.host_os.path.exists(filename):
      self.create(filename)
    else:
      self._fh = open(filename, mode)
    return self

  def close(self):
    self._fh.close()

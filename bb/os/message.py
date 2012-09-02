#!/usr/bin/env python

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'
__author__ = 'Oleksandr Sviridenko'

from bb.lib.utils import typecheck

class Message(object):
  """This class describes message structure passed between threads for
  communication purposes within OS. The message consists of ID represented by
  string and a set of fields, where each field described by class Field.
  """

  class Field(object):
    def __init__(self, name, size=0):
      if not typecheck.is_string(name):
        raise TypeError('Field name has to be a string')
      self._name = name
      self._size = 0
      if size:
        self.size = size

    @property
    def name(self):
      return self._name

    @property
    def size(self):
      return self._size

    @size.setter
    def size(self, size):
      self._size = size

  def __init__(self, id, fields):
    self._id = None
    self._fields = []
    if id:
      self.id = id
    if fields:
      self.fields = fields

  @property
  def id(self):
    return self._id

  @id.setter
  def id(self, id):
    if not typecheck.is_string(id):
      raise TypeError('`id` has to be a string')
    self._id = id

  @property
  def fields(self):
    return self._fields

  @fields.setter
  def fields(self, fields):
    self._fields = []
    if not typecheck.is_sequence(fields):
      raise TypeError('`fields` has to be a sequence')
    for field in fields:
      if typecheck.is_sequence(field):
        field = self.Field(field[0], field[1])
      elif not isinstance(field, Field):
        field = self.Field(field)
      self._fields.append(field)

  def __str__(self):
    return '%s[id=%s,fields=(%s)]' % (self.__class__.__name__, self.id,
                                      ','.join([_.name for _ in self.fields]))

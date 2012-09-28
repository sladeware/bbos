#!/usr/bin/env python
#
# Copyright (c) 2012 Sladeware LLC
# http://www.bionicbunny.org/
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'
__author__ = 'Oleksandr Sviridenko'

"""The messages are used by OS as the base unit for inter-thread
communication. A new message can be created with help of Message class as
follows:

  echo = Message('ECHO', ('text', 2))

The message echo here has ID 'ECHO' and one field 'text' of 2 bytes. Once a new
message has been created it can be registered by thread:

  thread = Thread('DEMO', 'demo_runner', messages=[echo])
  print thread.get_messages()

Once all the threads were registered within a mapping, all the messages that
will be available within an OS can be obtained with help of
Mapping.get_messages().
"""

from bb.utils import typecheck

# TODO(d2rk): put ID under the other fields.

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

  def __init__(self, label, input_fields=[], output_fields=[]):
    self._label = None
    self._input_fields = []
    self._output_fields = []
    if label:
      self.label = label
    if input_fields:
      self.input_fields = input_fields
    if output_fields:
      self.output_fields = output_fields

  @property
  def label(self):
    return self._label

  @label.setter
  def label(self, label):
    if not typecheck.is_string(label):
      raise TypeError('`label` has to be a string')
    self._label = label

  @property
  def size(self):
    return self.get_size()

  def get_size(self):
    return max(sum([_.size for _ in self.input_fields]),
               sum([_.size for _ in self.output_fields]))

  @property
  def input_fields(self):
    return self._input_fields

  @input_fields.setter
  def input_fields(self, input_fields):
    self._input_fields = []
    if not typecheck.is_sequence(input_fields):
      raise TypeError('`input_fields` has to be a sequence')
    for field in input_fields:
      if typecheck.is_sequence(field):
        field = self.Field(field[0], field[1])
      elif not isinstance(field, Field):
        field = self.Field(field)
      self._input_fields.append(field)

  @property
  def output_fields(self):
    return self._output_fields

  @output_fields.setter
  def output_fields(self, output_fields):
    self._output_fields = []
    if not typecheck.is_sequence(output_fields):
      raise TypeError('`output_fields` has to be a sequence')
    for field in output_fields:
      if typecheck.is_sequence(field):
        field = self.Field(field[0], field[1])
      elif not isinstance(field, Field):
        field = self.Field(field)
      self._output_fields.append(field)

  def __str__(self):
    return '%s[label=%s, size=%d, input_fields=(%s)]' % \
        (self.__class__.__name__, self.label, self.size,
         ','.join([_.name for _ in self.input_fields]))

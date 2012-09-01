#!/usr/bin/env python

from bb.tools.generators.generator import Generator

class CGenerator(Generator):
  def write_header(self, data, level=1):
    if level == 1:
      self.writeln('/' + '*' * 80)
      for line in data.split('\n'):
        self.writeln(' * ' + line)
      self.writeln(' ' + '*' * 79 + '/')
      self.writeln()
    elif level == 2:
      self.writeln('/' * 80)
      for line in data.split('\n'):
        self.writeln('// ' + line)

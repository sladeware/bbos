#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

from bb.testing import unittest
from bb.utils import executable

DEFAULT_PROGRAM_OPTIONS = executable.ExecutableOptions(
  verbose=False
)

def ProgramOptions():
  options = executable.ExecutableOptions()
  options.update(DEFAULT_PROGRAM_OPTIONS)
  return options

class Program(executable.ExecutableWrapper,
              executable.OptionsReaderInterface):

  OPTION_HANDLERS = {
    "verbose": "be_verbose"
    }

  def __init__(self):
    self.verbose = False

  def be_verbose(self, value=None):
    if value:
      self.verbose = value
    return self.verbose

class ExecutableOptionsTest(unittest.TestCase):

  def test_program_options(self):
    program = Program()
    options = ProgramOptions()
    program.read_options(options)
    self.assert_false(options["verbose"])
    self.assert_raises(TypeError, options.update, {"verbose": 1})

if __name__ == "__main__":
  unittest.main()

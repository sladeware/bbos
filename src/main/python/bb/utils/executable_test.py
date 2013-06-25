# http://www.bionicbunny.org/
# Copyright (c) 2012-2013 Sladeware LLC
#
# Author: Oleksandr Sviridenko

from bb.utils.testing import unittest
from bb.utils import executable

DEFAULT_PROGRAM_PARAMS = executable.ExecutableParams(
  verbose=False
)

def ProgramParams():
  params = executable.ExecutableParams()
  params.update(DEFAULT_PROGRAM_PARAMS)
  return params

class Program(executable.ExecutableWrapper,
              executable.ParamsReaderInterface):

  param_handlers = {
    "verbose": "be_verbose"
    }

  def __init__(self):
    executable.ExecutableWrapper.__init__(self, "echo")
    self.verbose = False

  def be_verbose(self, value=None):
    if value:
      self.verbose = value
    return self.verbose

class ExecutableParamsTest(unittest.TestCase):

  def test_program_params(self):
    program = Program()
    params = ProgramParams()
    program.read_params(params)
    self.assert_false(params["verbose"])
    #self.assert_raises(TypeError, params.update, {"verbose": 1})

if __name__ == "__main__":
  unittest.main()

# http://www.bionicbunny.org/
# Copyright (c) 2012-2013 Sladeware LLC

import tempfile

from bb.utils.testing import unittest
from bb.tools.compilers.propgcc import PropGCC

HELLO_WORLD_PROGRAM_MESSAGE = "Hello world!"
HELLO_WORLD_PROGRAM = """
#include <stdio.h>

int main()
{
  printf("%s");
  return 0;
}
""" % HELLO_WORLD_PROGRAM_MESSAGE

class PropGCCTest(unittest.TestCase):

  def setup(self):
    self._continue = PropGCC().check_executable()

  def test_compiling(self):
    if not self._continue:
      return
    input_fh = tempfile.NamedTemporaryFile(suffix=".c", delete=True)
    output_fh = tempfile.NamedTemporaryFile(suffix=".out", delete=False)
    compiler = PropGCC()
    compiler.set_output_filename(output_fh.name)
    input_fh.write(HELLO_WORLD_PROGRAM)
    input_fh.seek(0)
    ok = True
    try:
      compiler.compile(files=[input_fh.name])
    except Exception, e:
      ok = False
    input_fh.close()
    output_fh.close()
    self.assert_true(ok)

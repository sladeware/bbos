# http://www.bionicbunny.org/
# Copyright (c) 2012-2013 Sladeware LLC
#
# Author: Oleksandr Sviridenko

import os
import tempfile
import subprocess

from bb.utils.testing import unittest
from bb.utils import path_utils
from bb.utils import logging
from bb.tools.compilers.cc import CC

HELLO_WORLD_PROGRAM_MESSAGE = "Hello world!"
HELLO_WORLD_PROGRAM = """
#include <stdio.h>

int main()
{
  printf("%s");
  return 0;
}
""" % HELLO_WORLD_PROGRAM_MESSAGE

# Turn off logging
logger = logging.get_logger("bb")
logger.propagate = False

class CCTest(unittest.TestCase):

  def test_compile(self):
    input_fh = tempfile.NamedTemporaryFile(suffix=".c", delete=True)
    output_fh = tempfile.NamedTemporaryFile(suffix=".out", delete=False)
    compiler = CC()
    compiler.set_output_filename(output_fh.name)
    input_fh.write(HELLO_WORLD_PROGRAM)
    # We have to rewind the file handle using seek() in order to read the data
    # back from it!
    input_fh.seek(0)
    ok = True
    try:
      compiler.compile(files=[input_fh.name])
    except Exception, e:
      ok = False
      print e
    input_fh.close()
    output_fh.close()
    if ok:
      self.assert_equal(subprocess.check_output([output_fh.name]),
                        HELLO_WORLD_PROGRAM_MESSAGE)
    # Cleanup output temp file yourserlf
    os.remove(output_fh.name)
    self.assert_true(ok)
    #path_utils.remove_tree(compiler.get_build_dir_path())

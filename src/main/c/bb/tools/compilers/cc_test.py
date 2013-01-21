#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

import tempfile
import subprocess

import bb.utils
from bb import host_os
from bb.testing import unittest
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

class CCTest(unittest.TestCase):

  def test_compile(self):
    input_fh = tempfile.NamedTemporaryFile(suffix=".c", delete=True)
    output_fh = tempfile.NamedTemporaryFile(suffix=".out", delete=False)
    compiler = CC()
    compiler.set_output_file_path(output_fh.name)
    input_fh.write(HELLO_WORLD_PROGRAM)
    # We have to rewind the file handle using seek() in order to read the data
    # back from it!
    input_fh.seek(0)
    ok = True
    try:
      compiler.compile(sources=[input_fh.name])
    except Exception, e:
      ok = False
      print e
    input_fh.close()
    output_fh.close()
    if ok:
      self.assert_equal(subprocess.check_output([output_fh.name]),
                        HELLO_WORLD_PROGRAM_MESSAGE)
    # Cleanup output temp file yourserlf
    host_os.remove(output_fh.name)
    self.assert_true(ok)
    bb.utils.host_os.path.remove_tree(compiler.get_build_dir_path())

if __name__ == "__main__":
  unittest.main()

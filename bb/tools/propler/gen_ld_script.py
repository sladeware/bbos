#!/usr/bin/env python

"""Generate proper script for GNU linker (ld)."""

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'
__author__ = 'Olexander Sviridenko'

import os.path
from string import Template

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_FNAME = os.path.abspath(os.path.join(SCRIPT_DIR,
                                              "template_ld_script.ld"))

DEFAULT_VARS = dict(
  HUB_START_ADDRESS = 0,
  HUB_LEN = 32 * 1024,
)

def generate(output_fname, required_vars=dict()):
  fh = open(TEMPLATE_FNAME)
  template = Template(fh.read())
  fh.close()
  target_vars = DEFAULT_VARS
  target_vars.update(required_vars)
  output_fh = open(output_fname, "w")
  output_fh.write(template.safe_substitute(target_vars))
  output_fh.close()

if __name__ == "__main__":
  generate("script.ld", dict(HUB_START_ADDRESS=1024))

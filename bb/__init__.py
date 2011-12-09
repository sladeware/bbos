#!/usr/bin/env python

from __future__ import absolute_import

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

import os
import sys

#_______________________________________________________________________________

os.environ["BB_HOME"] = \
  os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))

#_______________________________________________________________________________
# Compatibility with Python 2.5 through 2.7.

assert (2,5) <= sys.version_info < (3,), """\
This code is meant for Python 2.5 through 2.7.
You might find that the parts you care about still work in older
Pythons or happen to work in newer ones, but you're on your own --
edit __init__.py if you want to try it."""


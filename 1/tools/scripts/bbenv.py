#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

import os
import sys

SCRIPT_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

# Setup the path properly for bbos builder imports 

# Define BBHOME environment variable
if not os.environ.has_key('BBHOME'):
    os.environ['BBHOME'] = os.path.join(SCRIPT_DIR, '..', '..')
sys.path = [os.environ["BBHOME"]] + sys.path

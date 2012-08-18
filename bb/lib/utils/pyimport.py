#!/usr/bin/env python

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'

import os
import sys

def get_fullname_by_path(path):
  fullname = None
  for search_path in sys.path:
    if path.startswith(search_path):
      mod_location = path[len(search_path) + 1:]
      parts = mod_location.split(os.sep)
      parts[-1] = parts[-1].split('.')[0] # remove extension
      fullname = '.'.join(parts)
  return fullname

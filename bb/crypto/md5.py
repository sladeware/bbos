#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

from hashlib import md5

def md5sum(filename, buf_size=8192):
  m = md5()
  # The with statement makes sure the file will be closed.
  with open(filename) as f:
    # Read the file in small chunk until EOF.
    data = f.read(buf_size)
    while data:
      m.update(data)
      data = f.read(buf_size)
  # Return the md5 hash in hexadecimal format.
  return m.hexdigest()

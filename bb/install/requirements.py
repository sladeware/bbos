#!/usr/bin/env python

from bb.utils import module
from bb.utils import module_manager

REQUIRED_MODULES = {
  "serial": {
    "version": None,
    "error_msg": "please download and install pyserial from http://pyserial.sourceforge.net",
    },
  "networkx": {
    "version": "1.5",
    "error_msg": "please download and install networkx library from http://networkx.lanl.gov",
    }
}

def check_all():
  print "Checking required modules:"
  missing = module_manager.check_missing(REQUIRED_MODULES)
  for name, info in REQUIRED_MODULES.items():
    if name in missing:
      msg = info.get("err_msg", "[NOT FOUND]")
      print "* '%s'... %s" % (name, msg)
      continue
    print "* '%s'... [OK]" % (name,)
  if missing:
    print "Sorry, but BB cannot be installed"
    exit(1)

# -*- coding: utf-8; -*-
#
# Copyright (c) 2013 Sladeware LLC
# http://www.bionicbunny.org/

from __future__ import with_statement, print_function

import os
try:
  import ConfigParser
except ImportError:
  import configparser as ConfigParser
import types

__all__ = ["read_user_settings", "gen_default_user_config", "UserConfigParser"]

USER_CONFIG_FILE_NAME = '.bbconfig'
_DEFAULT_USER_CONFIG_FILE_PATH = os.path.expanduser(os.path.join('~', USER_CONFIG_FILE_NAME))

_DEFAULT_USER_CONFIG = {
  "bbos": {
    "homedir": "",
  },
  "b3": {
    "builddir": "",
  }
}

def read_user_settings(path=_DEFAULT_USER_CONFIG_FILE_PATH):
  if not os.path.exists(path):
    gen_default_user_config(path)
  return UserConfigParser(path)

def gen_default_user_config(path=_DEFAULT_USER_CONFIG_FILE_PATH):
  if not type(path) is types.StringType:
    raise TypeError()
  if os.path.exists(path):
    return
  with open(path, "w") as handle:
    config = UserConfigParser(path)
    for section, options in _DEFAULT_USER_CONFIG.items():
      config.add_section(section)
      for option, value in options.items():
        config.set(section, option, value)
    config.write(handle)
  return path

class UserConfigParser(ConfigParser.SafeConfigParser):
  """Encapsulates user's ini-style config file."""

  def __init__(self, path):
    if not type(path) is types.StringType:
      raise TypeError()
    if not os.path.exists(path):
      raise OSError()
    ConfigParser.SafeConfigParser.__init__(self)
    with open(path) as config:
      self.readfp(config, filename=path)
    self._path = path

  def __del__(self):
    self.write()

  get_sections = ConfigParser.SafeConfigParser.sections
  write_to = ConfigParser.SafeConfigParser.write

  def write(self, handle=None):
    if not handle:
      with open(self._path, "w") as handle:
        self.write_to(handle)
    else:
      if not isinstance(handle, types.FileType):
        raise TypeError()
      self.write_to(handle)

  def dump(self):
    print("Dump cofig", self._path)
    for section in self.get_sections():
      print("[%s]" % section)
      for name, value in self.items(section):
        print("%s = %s" % (name, value))

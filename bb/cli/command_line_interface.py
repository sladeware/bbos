#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

class CommandLineInterface(object):
  config = None
  commands = dict()

  def __init__(self):
    pass

  @classmethod
  def get_commands(klass):
    return klass.commands.values()

  @classmethod
  def get_command_names(klass):
    return klass.commands.keys()

  @classmethod
  def register_command(klass, name, command):
    klass.commands[name] = command

  @classmethod
  def is_supported_command(klass, name):
    return name in klass.get_command_names()

  @classmethod
  def get_command(klass, name):
    return klass.commands[name]

  @classmethod
  def get_command_descriptions(klass):
    """Returns a formatted string containing the short_descs for all commands."""
    cmd_names = klass.commands.keys()
    cmd_names.sort()
    desc = ''
    max_cmd_name_len = 0
    for cmd_name in cmd_names:
      if len(cmd_name) > max_cmd_name_len:
        max_cmd_name_len = len(cmd_name)
    cmd_desc_frmt = '  %{0}s  %s\n'.format(max_cmd_name_len)
    for cmd_name in cmd_names:
      if not klass.commands[cmd_name].hidden:
        desc += cmd_desc_frmt % (cmd_name,
                                klass.commands[cmd_name].short_desc)
    return desc

  @classmethod
  def command(klass, usage, short_desc, uses_basepath=False,
              options=lambda obj, parser: None):
    def _(function):
      cmd = Command(function, usage, short_desc, uses_basepath,
                    options=options)
      klass.register_command(function.__name__, cmd)
      return function
    return _

CLI = CommandLineInterface

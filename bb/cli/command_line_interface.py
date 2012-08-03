#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

class Command(object):
  def __init__(self, function, usage, short_desc, long_desc='',
               error_desc=None, options=lambda obj, parser: None,
               uses_basepath=True, hidden=False):
    self.function = function
    self.usage = usage
    self.short_desc = short_desc
    self.long_desc = long_desc
    self.error_desc = error_desc
    self.options = options
    self.uses_basepath = uses_basepath
    self.hidden = hidden

  def __call__(self):
    return self.function()

  def get_descriptions(klass):
    """Returns a formatted string containing the short_descs for all commands."""
    command_names = klass.action_register.keys()
    action_names.sort()
    desc = ''
    for action_name in action_names:
      if not klass.action_register[action_name].hidden:
        desc += '  %s: %s\n' % (action_name,
                                klass.action_register[action_name].short_desc)
    return desc

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

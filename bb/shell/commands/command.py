#!/usr/bin/env python

class Command(object):
  USAGE = None
  SHORT_DESC = None
  LONG_DESC = ''
  ERROR_DESC = None
  USES_BASEPATH = True
  HIDDEN = False

  def __init__(self):
    self.usage = self.USAGE
    self.short_desc = self.SHORT_DESC
    self.long_desc = self.LONG_DESC
    self.error_desc = self.ERROR_DESC
    self.uses_basepath = self.USES_BASEPATH
    self.hidden = self.HIDDEN

  def __call__(self):
    return self.function()

  def options(self, config, optparser):
    pass

  def function(self):
    raise NotImplementedError

  def get_descriptions(self):
    """Returns a formatted string containing the short_descs for all commands.
    """
    command_names = klass.action_register.keys()
    action_names.sort()
    desc = ''
    for action_name in action_names:
      if not klass.action_register[action_name].hidden:
        desc += '  %s: %s\n' % (action_name,
                                klass.action_register[action_name].short_desc)
    return desc

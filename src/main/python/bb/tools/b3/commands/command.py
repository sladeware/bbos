# -*- coding: utf-8; -*-
#
# http://www.bionicbunny.org/
# Copyright (c) 2013 Sladeware LLC
#
# Author: Oleksandr Sviridenko <info@bionicbunny.org>

class Command(object):

  def __init__(self, root_dir, parser, args):
    """root_dir: The root directory of the pants workspace
    parser: an OptionParser
    argv: the subcommand arguments to parse
    """
    self.root_dir = root_dir
    # Override the OptionParser's error with more useful output
    def error(message = None, show_help = True):
      if message:
        print(message + '\n')
      if show_help:
        parser.print_help()
      parser.exit(status = 1)
    parser.error = error
    self.error = error
    self.setup_parser(parser, args)
    self.options, self.args = parser.parse_args(args)
    self.parser = parser

  def setup_parser(self, parser, args):
    """Subclasses should override and confiure the OptionParser to reflect the
    subcommand option and argument requirements.  Upon successful construction,
    subcommands will be able to access self.options and self.args.
    """
    pass

  @classmethod
  def serialized(cls):
    return False

  def error(self, message = None, show_help = True):
    """Reports the error message, optionally followed by pants help, and then
    exits.
    """

  def run(self, lock):
    """Subcommands that are serialized() should override if they need the
    ability to interact with the global command lock.  The value returned should
    be an int, 0 indicating success and any other value indicating failure.
    """
    return self.execute()

  def execute(self):
    """Subcommands that do not require serialization should override to perform
    the command action.  The value returned should be an int, 0 indicating
    success and any other value indicating failure.
    """
    raise NotImplementedError('Either run(lock) or execute() must be over-ridden.')

  def cleanup(self):
    """Called on SIGINT (e.g., when the user hits ctrl-c). Subcommands may
    override to perform cleanup before exit.
    """
    pass

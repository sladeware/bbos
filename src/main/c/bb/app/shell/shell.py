#!/usr/bin/env python
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

import logging
import optparse
import sys

from bb.app.shell.commands import DEFAULT_COMMANDS

class OptionError(optparse.OptionError):
  pass

class OptionParser(optparse.OptionParser):

  def error(self, msg):
    raise Exception(msg)

class Shell(object):
  """Application shell.

  optparser: An instnace of :class:`OptionParser`
  argv: The original command line as a list.
  args: The positional command line args left over after parsing
  the options.
  raw_input_fn: Function used for getting raw user input.
  error_fh: Unexpected errors are printer to this file handle.
  """

  def __init__(self, argv=sys.argv, optparser_class=OptionParser,
               raw_input_fn=raw_input, out_fh=sys.stdout, error_fh=sys.stderr):
    self.argv = argv
    self.optparser_class = optparser_class
    self.raw_input_fn = raw_input_fn
    self.out_fh = out_fh
    self.error_fh = error_fh
    self.args = dict()
    self.options = optparse.Values()
    self.optparser = self._get_default_optparser()
    self.command = None
    self._commands = dict()
    self._register_default_commands()

  def _register_default_commands(self):
    for command in DEFAULT_COMMANDS:
      self.register_command(command)

  def parse_command_line(self, argv=sys.argv):
    try:
      self.options, self.args = self.optparser.parse_args(argv[1:])
    except Exception, msg:
      self.args = argv[1:]
    if len(self.args) < 1:
      self._print_help_and_exit()
    if getattr(self.options, 'help', False):
      self._print_help_and_exit()
    cmd_name = self.args.pop(0)
    if not self.is_supported_command(cmd_name):
      print "Unknown command: '%s'\n" % (cmd_name, )
      self._print_help_and_exit(2)
    self.command = self.get_command(cmd_name)
    self.optparser, self.options = self._make_specific_parser(self.command)
    self.options, self.args = self.optparser.parse_args(argv[1:])

  def get_option(self, name, default=None):
    value = getattr(self.options, name, default)
    return value

  def _print_help_and_exit(self, exit_code=0):
    self.optparser.print_help()
    print
    print "Commands:"
    print self.get_command_descriptions()
    print "See 'bionicbunny help <command>' for more information on a" \
        "specific command."
    sys.exit(exit_code)

  def _make_specific_parser(self, command):
    """Creates a new parser with documentation specific to `command` -- an
    Command instance to be used when initializing the new parser.

    Returns a tuple containing parser -- an instance of OptionsParser customized
    to 'command', and options -- the command line options after re-parsing.
    """
    parser = self._get_optparser()
    parser.set_usage(command.usage)
    parser.set_description('%s\n%s' % (command.short_desc, command.long_desc))
    command.options(self, parser)
    options, unused_args = parser.parse_args(self.argv[1:])
    return parser, options

  def _get_default_optparser(self):
    parser = self._get_optparser()
    parser.add_option('-h', '--help', action='store_true', dest='help',
                      help='Show the help message and exit.')
    parser.add_option('-v', '--verbose', action='store_true', dest='verbose',
                      help='Be verbose')
    #parser.add_option("--multiterminal", action="store_true",
    #                  dest="multiterminal",
    #                  help="Open each new running OS in a new terminal. "\
    #                      "(only Linux)")
    return parser

  def _get_optparser(self):
    class Formatter(optparse.IndentedHelpFormatter):
      def format_description(self, description):
        return description + '\n'
    parser = self.optparser_class(usage='%prog [options] <command> [<args>]',
                                  formatter=Formatter(),
                                  conflict_handler='resolve')
    return parser

  def run(self):
    self.parse_command_line()
    self.command(*self.args[1:])

  def get_commands(self):
    return self._commands.values()

  def get_command_names(self):
    return self._commands.keys()

  def register_command(self, command, name=None):
    if not name:
      name = command.__class__.__name__
    self._commands[name] = command

  def is_supported_command(self, name):
    return name in self.get_command_names()

  def get_command(self, name):
    return self._commands[name]

  def get_command_descriptions(self):
    """Returns a formatted string containing the short description for all
    commands.
    """
    cmd_names = self._commands.keys()
    cmd_names.sort()
    desc = ''
    max_cmd_name_len = 0
    for cmd_name in cmd_names:
      if len(cmd_name) > max_cmd_name_len:
        max_cmd_name_len = len(cmd_name)
    cmd_desc_frmt = "  %{0}s  %s\n".format(max_cmd_name_len)
    for cmd_name in cmd_names:
      if not self._commands[cmd_name].hidden:
        desc += cmd_desc_frmt % (cmd_name, self._commands[cmd_name].short_desc)
    return desc

  def command(self, usage, short_desc, uses_basepath=False,
              options=lambda obj, parser: None):
    def _(function):
      cmd = Command(function, usage, short_desc, uses_basepath,
                    options=options)
      self.register_command(cmd, function.__name__)
      return function
    return _

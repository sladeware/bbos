#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

import optparse
import logging
import sys

import bb
from bb.config import host_os
from bb.cli.command_line_interface import CLI

class Config(object):
    """Class to wrap bb-script functionality.

    Attributes:
    optparser: An instnace of :class:`optparse.OptionParser`
    argv: The original command line as a list.
    args: The positional command line args left over after parsing
    the options.
    raw_input_fn: Function used for getting raw user input.
    error_fh: Unexpected errors are printer to this file handle.
    """

    def __init__(self, argv=sys.argv, optparser_class=optparse.OptionParser,
                 raw_input_fn=raw_input,
                 out_fh=sys.stdout,
                 error_fh=sys.stderr):
        self.argv = argv
        self.optparser_class = optparser_class
        self.raw_input_fn = raw_input_fn
        self.out_fh = out_fh
        self.error_fh = error_fh
        self.args = dict()
        self.options = optparse.Values()
        self.optparser = self._get_default_optparser()
        self.command = None
        #for command in CLI.get_commands():
        #    command.options(self, self.optparser)

    def parse_command_line(self, argv=sys.argv):
        self.options, self.args = self.optparser.parse_args(argv[1:])
        if len(self.args) < 1:
            self._print_help_and_exit()
        if self.options.help:
            self._print_help_and_exit()
        command_name = self.args.pop(0)
        if not CLI.is_supported_command(command_name):
            self.optparser.error("Unknown command: '%s'\n" %
                                 (command_name, ))
        self.command = CLI.get_command(command_name)
        self.optparser, self.options = self._make_specific_parser(self.command)

    def get_option(self, name, default=None):
        value = getattr(self.options, name, default)
        return value

    def _print_help_and_exit(self, exit_code=2):
        self.optparser.print_help()
        print
        print "Commands:"
        print CLI.get_command_descriptions()
        print "See 'bionicbunny help <command>' for more information on a" \
            "specific command."
        sys.exit(exit_code)

    def _make_specific_parser(self, command):
        """Creates a new parser with documentation specific to 'command'.

        Args:
        command: An Command instance to be used when initializing the new parser.

        Returns:
        A tuple containing:
        parser: An instance of OptionsParser customized to 'command'.
        options: The command line options after re-parsing.
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

CLI.config = Config()

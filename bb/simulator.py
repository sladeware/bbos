#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

import optparse
import sys

class Config(object):
    """Class to wrap simulator functionality.

    Attributes:
    optparser: An instnace of optparse.OptionParser
    argv: The original command line as a list.
    args: The positional command line args left over after parsing the options.
    raw_input_fn: Function used for getting raw user input.
    error_fh: Unexpected errors are printer to this file handle.
    """

    def __init__(self, optparser_class=optparse.OptionParser,
                 raw_input_fn=raw_input,
                 out_fh=sys.stdout,
                 error_fh=sys.stderr):
        self.argv = None
        self.optparser_class = optparser_class
        self.raw_input_fn = raw_input_fn
        self.out_fh = out_fh
        self.error_fh = error_fh
        self.args = {}
        self.options = optparse.Values()
        self.optparser = self._get_optparser()

    def parse_command_line(self, argv=sys.argv):
        self.options, self.args = self.optparser.parse_args(argv[1:])
        if self.options.help:
            self._print_help_and_exit()

    def get_option(self, name, default=None):
        value = getattr(self.options, name, default)
        return value

    def _print_help_and_exit(self, exit_code=2):
        self.optparser.print_help()
        sys.exit(exit_code)

    def _get_optparser(self):
        class Formatter(optparse.IndentedHelpFormatter):
            def format_description(self, description):
                return description, '\n'
        parser = self.optparser_class(usage='%prog [Options]',
                                      formatter=Formatter(),
                                      conflict_handler='resolve')
        parser.add_option('-h', '--help', action='store_true', dest='help',
                          help='Show the help message and exit.')
        parser.add_option("--multiterminal", action="store_true",
                          dest="multiterminal",
                          help="Open each new running mapping a new terminal. "\
                              "Supports Linux.")
        return parser

config = Config()

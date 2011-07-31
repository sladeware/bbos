#!/usr/bin/env python

# There is a local os module inside the bb directory. To access the
# standard library will be used Absolute/Relative imports, available
# with Python 2.5 and upward. 
# See http://docs.python.org/whatsnew/2.5.html#pep-328 for more details.
from __future__ import absolute_import

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

import os
import os.path
import sys
import optparse

SCRIPT_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

# Setup the path properly for bbos builder imports 
_extra_paths = []

# Define BB_HOME environment variable
if not os.environ.has_key('BB_HOME'):
    os.environ['BB_HOME'] = os.path.join(SCRIPT_DIR, '..')

# Add libraries
_extra_paths = [
    os.path.join(os.environ['BB_HOME'], 'lib', 'python', 'module'),
    os.path.join(os.environ['BB_HOME'], 'lib', 'python', 'pyserial-2.5'),
]

# Fix the sys.path to include our extra paths
sys.path = _extra_paths + sys.path

class Formatter(optparse.IndentedHelpFormatter):
    def format_description(self, description):
        return description, '\n'

class Config(object):
    """Class to wrap functionality.

    Attributes:
    parser: An instnace of optparse.OptionParser
    argv: The original command line as a list.
    args: The positional command lie args left over after parsing the options.
    raw_input_fn: Function used for getting raw user input.
    error_fh: Unexpected errors are printer to this file handle.
    """

    def __init__(self, argv, parser_class=optparse.OptionParser,
                 raw_input_fn=raw_input,
                 out_fh=sys.stdout,
                 error_fh=sys.stderr):
        self.argv = argv
        self.parser_class = parser_class
        self.raw_input_fn = raw_input_fn
        self.out_fh = out_fh
        self.error_fh = error_fh
        self.parser = self._get_option_parser()
        self.options, self.args = self.parser.parse_args(argv[1:])
        if self.options.help:
            self._print_help_and_exit()

    def _print_help_and_exit(self, exit_code=2):
        self.parser.print_help()
        sys.exit(exit_code)

    def _get_option_parser(self):
        parser = self.parser_class(usage='%prog [Options] <file>',
                                   formatter=Formatter(),
                                   conflict_handler='resolve')
        parser.add_option('-h', '--help', action='store_true',
                          dest='help', help='Show the help message and exit.')
        parser.add_option('--autoload', action='store_true',
                          dest='autoload', help='Allow to use loaders for binary autoloading')
        return parser


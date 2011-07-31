
__copyright__ = "Copyright (c) 2011 Sladeware LLC"

import optparse
import sys

class Config(object):
    """Class to wrap build-script functionality.

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
        class Formatter(optparse.IndentedHelpFormatter):
            def format_description(self, description):
                return description, '\n'

        parser = self.parser_class(usage='%prog [Options]',
                                   formatter=Formatter(),
                                   conflict_handler='resolve')
        parser.add_option('-h', '--help', action='store_true',
                          dest='help', help='Show the help message and exit.')
        parser.add_option('--autoload', action='store_true',
                          dest='autoload', help='Allow to use loaders for binary autoloading.')
        parser.add_option('--dry-run', action='store_true',
                          dest='dry_run', help='Show only messages that would be printed in a real run.')
        return parser

config = Config(sys.argv)



__copyright__ = "Copyright (c) 2011 Sladeware LLC"

import optparse
import sys

import bb

class Config(bb.Config):
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


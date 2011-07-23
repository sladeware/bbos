#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

import sys
import getopt

import bbenv
from bb import os

FLAG_SPEC = (['help'] + ['print-commands'])

def usage():
    pass

def print_commands(target_file):
    mod = os.importer(target_file)
    print "Supported commands:"
    for command in mod.get_commands():
        print " ", command.get_name()

def main(argv=None):
    """The main entry point for the script."""
    target_files = []
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h:", FLAG_SPEC)
            if not len(opts) and not len(args):
                usage()
        except getopt.error, msg:
            raise Exception(msg)
        for target_file in args:
            target_files.append(target_file)
        for o, a in opts:
            if o in ("-h", "--help"):
                usage()
                exit(0)
            elif o in ('--print-commands'):
                for target_file in target_files:
                    print_commands(target_file)
            else:
                raise Exception("Unhandled argument")
    except Exception, err:
        print >>sys.stderr, err
        print >>sys.stderr, "for help use --help"
        return 2
    return 0

if __name__=='__main__':
    sys.exit(main())

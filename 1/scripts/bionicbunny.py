#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

import sys
import os
import getopt
import os.path
import hashlib
import imp
import traceback

import bbenv

#_______________________________________________________________________________

def usage():
    print'''Welcome to the Bionic Bunny platform!

USAGE: bb.py [OPTIONS] [FILES]

-h, --help  : print this help message
'''

def touch(target_file):
    """Execute the file at the specified path. 

    When we use Python directly it automatically adds the directory containing 
    the script that was used to invoke the Python interpreter to the search 
    path for modules. Therefore we will compensate this and for each target_file
    on the time when it's running its directory will be added to the search 
    path."""
    target_dir = os.path.abspath(os.path.dirname(os.path.realpath(target_file)))
    sys.path = [target_dir] + sys.path
    try:
        imp.load_source(hashlib.md5(target_file).hexdigest(), target_file)
    except:
        traceback.print_exc(file=sys.stderr)
        raise
    # Sefely remove target_dir from the search path
    sys.path.remove(target_dir)

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h:", ["help"])
            if not len(opts) and not len(args):
                usage()
        except getopt.error, msg:
            raise Exception(msg)
        for o, a in opts:
            if o in ("-h", "--help"):
                usage()
            else:
                raise Exception("Unhandled argument")
        for target_file in args:
            touch(target_file)
    except Exception, err:
        print >>sys.stderr, err
        print >>sys.stderr, "for help use --help"
        return 2
    return 0

if __name__ == '__main__':
    sys.exit(main())

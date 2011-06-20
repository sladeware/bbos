#!/usr/bin/python

__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

import sys
import os
import getopt
import os.path
import hashlib
import imp
import traceback

SCRIPT_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

# Setup the path properly for bb platform imports
if not os.environ.has_key('BBHOME'):
    os.environ['BBHOME'] = os.path.join(SCRIPT_DIR, "..")
    sys.path = [os.environ["BBHOME"]] + sys.path
else:
    sys.path.insert(0, os.environ['BBHOME'])

def usage():
    print'''Welcome to the Bionic Bunny platform!

USAGE: bb.py [OPTIONS] [FILES]

-h, --help  : print this help message
'''

def touch(py_path):
    try:
        application = imp.load_source(hashlib.md5(py_path).hexdigest(), py_path)
    except:
        traceback.print_exc(file=sys.stderr)
        raise

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
        for application in args:
            touch(application)
    except Exception, err:
        print >>sys.stderr, err
        print >>sys.stderr, "for help use --help"
        return 2
    return 0

if __name__ == '__main__':
    sys.exit(main())

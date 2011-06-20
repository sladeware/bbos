#!/usr/bin/python

__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

import sys
import os
import getopt
import os.path
import hashlib
import imp
import traceback

if not hasattr(sys, 'version_info'):
    sys.stderr.write('Very old versions of Python are not supported. Please '
                     'use version 2.5 or greater.\n')
    sys.exit(1)
version_tuple = tuple(sys.version_info[:2])
if version_tuple < (2, 4):
    sys.stderr.write('Error: Python %d.%d is not supported. Please use '
                     'version 2.5 or greater.\n' % version_tuple)
    sys.exit(1)

SCRIPT_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

# Setup the path properly for bb platform imports
if not os.environ.has_key('BBHOME'):
    os.environ['BBHOME'] = os.path.join(SCRIPT_DIR, "..")
sys.path = [os.environ["BBHOME"]] + sys.path

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

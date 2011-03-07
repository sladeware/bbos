#!/usr/bin/python

import sys
import os
import getopt
import os.path
import hashlib
import imp
import traceback

# Setup the path properly for bbos builder imports
if not os.environ.has_key('BBOSHOME'):
    path = os.path.abspath(os.path.dirname(sys.argv[0])) + "/.."
    sys.path.insert(0, path)
    os.environ['BBOSHOME'] = path
else:
    sys.path.insert(0, os.environ['BBOSHOME'])

def usage():
    print'''Welcome to the Bionic Bunny Operating System!

USAGE: bbos.py [OPTIONS] [FILES]

-h, --help  : print this help message
'''

def touch(py_path):
    try:
        application = imp.load_source(hashlib.md5(py_path).hexdigest(), py_path)
    except ImportError:
        traceback.print_exc(file=sys.stderr)
        raise
    application_entry = application.main
    assert application_entry, "You must define main() in your application"
    try:
        application_entry()
    except:
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

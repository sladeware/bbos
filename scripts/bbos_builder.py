#!/usr/bin/python

"""Main program for generating code and building a BBOS application.
"""

__copyright__  = "Copyright (c) 2010 Slade Maurer, Alexander Sviridenko"

import sys
import getopt
import hashlib
import os.path
import imp
import traceback

# Setup the path properly for bbos builder imports
path = os.path.abspath(os.path.dirname(sys.argv[0])) + "/.."
sys.path.append(path)

from bbos.application import *
from bbos.builder.code_builder import *
from bbos.builder.code_generator import *
from bbos.builder.common import *

# Enable this for debugging when you don't want to remove files
DO_NOT_REMOVE = True

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def usage():
    print """
    Welcome to the Bionic Bunny Operating System Builder!
    
    USAGE: [OPTION]... [FILE]

    -h, --help : print this help message

    -a=FILE, --application_configuration=FILE : Load the application configuration from FILE
    """

# Dynamically load the user defined bbos.py module
def load_app_config(code_path):
    try:
        try:
            code_dir = os.path.dirname(code_path)

            fin = open(code_path, 'rb')

            return [code_dir, imp.load_source(hashlib.md5(code_path).hexdigest(), code_path, fin)]
        finally:
            try: fin.close()
            except: pass
    except ImportError:
        traceback.print_exc(file = sys.stderr)
        raise
    except:
        traceback.print_exc(file = sys.stderr)
        raise

def do_it(code_path):
    """Do the primary work of the BBOS builder; we generate and build code."""
    # Dynamically load the user defined bbos.py module and verify the output
    (directory, module) = load_app_config(code_path)
    verify_string(directory)
    application = module.application
    assert application, "You must define the application variable in bbos.py"
    assert isinstance(application, BBOSApplication), "The application variable must be a BBOSApplication type"

    for process in application.get_processes():
        print "Working on process \"%s\":" % process.name

        # Generate the late binding application source code
        g = GenerateCode(directory, process)
        g.generate()

        # Build the application code
        b = BuildCode(directory, process)
        b.build()

        # Cleanup after this process
        if not DO_NOT_REMOVE:
            header_file = directory + BBOS_HEADER
            print "Removing " + header_file + " ..."
            os.remove(header_file)

        print "\n"

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "ha:", ["help", "application_configuration="])
            if not len(opts) and not len(args):
                usage()
        except getopt.error, msg:
             raise Usage(msg)
        for o, a in opts:
            if o in ("-a", "--application_configuration"):
                do_it(a)
            elif o in ("-h", "--help"):
                usage()
            else:
                raise Usage("Unhandled argument")
        for a in args:
            do_it(a)
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())

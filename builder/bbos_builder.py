#!/usr/bin/python

"""Main program for generating code and building a BBOS application.
"""

__copyright__  = "Copyright (c) 2010 Slade Maurer, Alexander Sviridenko"

from lib.common import *
from lib.bbos_application import *
from lib.bbos_compiler import *
from lib.bbos_driver import *
from lib.bbos_code_builder import *
from lib.bbos_code_generator import *
from lib.bbos_process import *
import sys
import getopt
import md5
import os.path
import imp
import traceback


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def usage():
    print """
    Welcome to the Bionic Bunny Operating System Builder!
    
    -h, --help : print this help message
    -a=FILE, --application_configuration=FILE : Load the application configuration from FILE
    """

# Dynamically load the user defined bbos.py module
def load_app_config(code_path):
    try:
        try:
            code_dir = os.path.dirname(code_path)

            fin = open(code_path, 'rb')

            return [code_dir, imp.load_source(md5.new(code_path).hexdigest(), code_path, fin)]
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
        # Generate the late binding application source code
        g = GenerateCode(directory, process)
        g.generate()

        # Build the application code
        b = BuildCode(directory, process)
        b.build()

        # Cleanup after this process
        header_file = directory + BBOS_HEADER
        print "Removing " + header_file + " ..."
        os.remove(header_file)

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "ha:", ["help", "application_configuration="])
        except getopt.error, msg:
             raise Usage(msg)
        for o, a in opts:
            if o in ("-a", "--application_configuration"):
                do_it(a)
            elif o in ("-h", "--help"):
                usage()
            else:
                raise Usage("Unhandled argument")
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())

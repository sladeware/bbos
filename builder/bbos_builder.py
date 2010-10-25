#!/usr/bin/python
# 
# Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
#

from common import *
from bbos_application import *
from bbos_compiler import *
from bbos_driver import *
from bbos_code_builder import *
from bbos_code_generator import *
from bbos_process import *
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
            code_file = os.path.basename(code_path)

            fin = open(code_path, 'rb')

            return [code_dir, imp.load_source(md5.new(code_path).hexdigest(), code_path, fin)]
        finally:
            try: fin.close()
            except: pass
    except ImportError, x:
        traceback.print_exc(file = sys.stderr)
        raise
    except:
        traceback.print_exc(file = sys.stderr)
        raise

# Here we do the primary work of the BBOS builder -- i.e. generate and build code.
def do_it(code_path):
    # Dynamically load the user defined bbos.py module and verify the output
    (directory, module) = load_app_config(code_path)
    verify_string(directory)
    application = module.application
    assert application, "You must define the application variable in bbos.py"
    assert isinstance(application, BBOSApplication), "The application variable must be a BBOSApplication type"

    # Generate the late binding applicaiton source code
    g = GenerateCode(directory, application)
    assert g
    g.generate()

    # Builde the application code
    b = BuildCode(directory, application)
    assert b
    b.build()

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

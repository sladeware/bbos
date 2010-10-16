#!/usr/bin/python
# 
# Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
#

import BBOSApplication
import BBOSCompiler
import BBOSDriver
import BBOSProcess
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

def  load_app_config(code_path):
    try:
        try:
            code_dir = os.path.dirname(code_path)
            code_file = os.path.basename(code_path)

            fin = open(code_path, 'rb')

            return [code_path, imp.load_source(md5.new(code_path).hexdigest(), code_path, fin)]
        finally:
            try: fin.close()
            except: pass
    except ImportError, x:
        traceback.print_exc(file = sys.stderr)
        raise
    except:
        traceback.print_exc(file = sys.stderr)
        raise

def generate_code(config):
    code_path = config[0]
#    application.config[1].application
    print config[1]
    
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
                generate_code(load_app_config(a))
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

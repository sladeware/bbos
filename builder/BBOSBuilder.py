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

BBOS_H_TOP ="""
/*
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_H
#define __BBOS_H

#include <bbos/compiler.h>

"""

BBOS_H_BOTTOM ="""
#include <bbos/kernel.h>

#endif /* __BBOS_H */
"""

BBOS_SWITCHER_TOP="""
/* Application switcher macro */
#define bbos_application_switcher(id) \\
  switch(id) { \\
"""

BBOS_SWITCHER_BOTTOM="""    default: \\
      bbos_exit(); \\
  }
"""

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def usage():
    print """
    Welcome to the Bionic Bunny Operating System Builder!
    
    -h, --help : print this help message
    -a=FILE, --application_configuration=FILE : Load the application configuration from FILE
    """

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

def generate_code(config):
    app = config[1].BBOSConfiguration.application
    assert len(app.processes) == 1 # Until we can handle more than one process
    process = app.processes[0]
    f = open(config[0] + "/bbos.h", "w")

    # Output the static top content
    f.write(BBOS_H_TOP)

    # Output the thread IDs
    f.write("/* Thread IDs */\n")
    id = 0
    for thread in process.threads:
        f.write("#define " + thread.upper() + " " + str(id) + "\n")
        id += 1
    for driver in process.drivers:
        f.write("#define " + driver.name.upper() + " " + str(id) + "\n")
        id += 1

    # Output the number of app threads
    f.write("\n/* The number of BBOS application threads */\n")
    f.write("#define BBOS_NUMBER_OF_APPLICATION_THREADS " + str(id) + "\n")

    # Output the switcher macro
    f.write(BBOS_SWITCHER_TOP)
    for thread in process.threads:
        f.write("    case " + thread.upper() + ": \\\n")
        f.write("      " + thread + "(); \\\n")
        f.write("      break; \\\n")
    for driver in process.drivers:
        f.write("    case " + driver.name.upper() + ": \\\n")
        f.write("      " + driver.entry_function + "(); \\\n")
        f.write("      break; \\\n")
    f.write(BBOS_SWITCHER_BOTTOM)

    # Output the port IDs
    f.write("\n/* Port IDs */\n")
    id = 0
    for port in process.ports:
        f.write("#define " + port + " " + str(id) + "\n")
        id += 1
    for driver in process.drivers:
        f.write("#define " + driver.port + " " + str(id) + "\n")
        id += 1

    # Output the number of ports in this process
    f.write("\n/* The number of ports in this process */\n")
    f.write("#define BBOS_NUMBER_OF_PORTS " + str(id) + "\n")

    # Output the mempools
    f.write("\n/* Mempool IDs */\n")
    id = 0
    for mempool in process.mempools:
        f.write("#define " + mempool + " " + str(id) + "\n")
        id += 1

    # Output the number of mempools in this process
    f.write("\n/* The number of mempools in this process */\n")
    f.write("#define BBOS_NUMBER_OF_MEMPOOLS " + str(id) + "\n")

    # Output BBOS driver constants
    f.write("\n/* BBOS driver constants */\n")
    for driver in process.drivers:
        f.write("#define GPIO_DRIVER_NAME \"" + driver.name + "\"\n")
        f.write("#define GPIO_DRIVER_VERSION " + str(driver.version) + "\n")

    # Output the bootstrapper functions
    f.write("\n/* BBOS driver bootstrapper functions */\n")
    f.write("#define bbos_boot_drivers \\\n")
    for driver in process.drivers:
        f.write("    " + driver.boot_function + "(); \\\n")

    # Output the exit functions
    f.write("\n/* BBOS driver exit functions */\n")
    f.write("#define bbos_exit_drivers \\\n")
    for driver in process.drivers:
        f.write("    " + driver.exit_function + "(); \\\n")

    # Output the static bottom content
    f.write(BBOS_H_BOTTOM)

    f.close()
    
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

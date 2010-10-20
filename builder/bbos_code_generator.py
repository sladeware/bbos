#!/usr/bin/python
# 
# Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
#
# Generate the source code for the bbos.h header file used to late bind BBOS
# processes, threads and etc just before building. We need this since the
# C macro language is seriously underpowered for our purposes.
#

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


class GenerateCode:
    def __init__(self, config):
        self.config = config

    def generate(self):
        assert self.config[1].application, "You must define the application variable in bbos.py"

        assert len(self.config[1].application.processes) == 1, "Right now we can handle only one process."

        # The process we're genearting code for
        process = self.config[1].application.processes[0]

        # The list of threads within the process
        threads = process.threads + [d.name for d in process.drivers]

        # The list of main functions for each thread
        main_functions = process.threads + [d.main for d in process.drivers]

        # The list of ports
        ports = process.ports + [d.port for d in process.drivers]

        # Open the header file we're outputing to
        f = open(self.config[0] + "/bbos.h", "w")

        # Output the static top content
        f.write(BBOS_H_TOP)

        # Output the thread IDs
        f.write("/* Thread IDs */\n")
        for id in range(0, len(threads)):
            f.write("#define " + threads[id].upper() + " " + str(id) + "\n")

        # Output the number of app threads
        f.write("\n/* The number of BBOS application threads */\n")
        f.write("#define BBOS_NUMBER_OF_APPLICATION_THREADS " + str(len(threads)) + "\n")

        # Output the switcher macro
        f.write(BBOS_SWITCHER_TOP)
        for thread, main_function in zip(threads, main_functions):
            f.write("    case " + thread.upper() + ": \\\n")
            f.write("      " + main_function + "(); \\\n")
            f.write("      break; \\\n")
        f.write(BBOS_SWITCHER_BOTTOM)

        # Output the port IDs
        f.write("\n/* Port IDs */\n")
        for id in range(0, len(ports)):
            f.write("#define " + ports[id] + " " + str(id) + "\n")

        # Output the number of ports in this process
        f.write("\n/* The number of ports in this process */\n")
        f.write("#define BBOS_NUMBER_OF_PORTS " + str(len(ports)) + "\n")

        # Output the mempools
        f.write("\n/* Mempool IDs */\n")
        for id in range(0, len(process.mempools)):
            f.write("#define " + process.mempools[id] + " " + str(id) + "\n")

        # Output the number of mempools in this process
        f.write("\n/* The number of mempools in this process */\n")
        f.write("#define BBOS_NUMBER_OF_MEMPOOLS " + str(len(process.mempools)) + "\n")

        # Output BBOS driver constants
        f.write("\n/* BBOS driver constants */\n")
        for driver in process.drivers:
            f.write("#define GPIO_DRIVER_NAME \"" + driver.name + "\"\n")
            f.write("#define GPIO_DRIVER_VERSION " + str(driver.version) + "\n")

        # Output the bootstrapper functions
        f.write("\n/* BBOS driver bootstrapper functions */\n")
        f.write("#define bbos_boot_drivers \\\n")
        for driver in process.drivers:
            f.write("    " + driver.boot + "(); \\\n")

        # Output the exit functions
        f.write("\n/* BBOS driver exit functions */\n")
        f.write("#define bbos_exit_drivers \\\n")
        for driver in process.drivers:
            f.write("    " + driver.exit + "(); \\\n")

        # Output the includes for this process
        f.write("\n/* The include files we are using  */\n")
        for include in process.get_include_files():
            f.write("#include <" + include + ">\n")

        # Output the static bottom content
        f.write(BBOS_H_BOTTOM)

        f.close()

"""Class used to generate C source code used by BBOS for late binding.

Generate the source code for the bbos.h header file used to late bind BBOS
processes, threads and etc just before building. We need this since the
C macro language is seriously underpowered for our purposes.
"""

__copyright__ = "Copyright (c) 2010 Slade Maurer, Alexander Sviridenko"

from bbos.kernel.process.scheduler.static import *
from common import *
import sys
import tempfile
import traceback

BBOS_H_TOP ="""
/*
 * This is BBOS generated source code used for late binding application
 * features just before compile time.
 *
 * Please do not edit this by hand, as your changes will be lost.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_H
#define __BBOS_H

"""

BBOS_H_BOTTOM ="""
#include <bbos/kernel.h>

#endif /* __BBOS_H */
"""

BBOS_STATIC_SCHEDULER_TOP="""
/* Application static scheduler macro */
#define BBOS_SCHEDULER_STATIC
#define bbos_static_scheduler()  \\
  while(true) { \\
"""

BBOS_STATIC_SCHEDULER_BOTTOM="  }\n"


class GenerateCode:
    def __init__(self, directory, process, test=False):
        # The process we're generating code for
        self.process = process

        # The list of threads within the process
        self.threads = self.process.threads + [d.name for d in self.process.drivers]

        # The list of ports
        if self.process.drivers:
            for ports in [d.ports for d in self.process.drivers]:
                self.ports = self.process.ports + ports
        else:
            self.ports = []

        self.test = test

        if not self.test:
            self.test = False
            # Open the header file we're outputing to
            filename = directory + BBOS_HEADER
            try:
                self.f = open(filename, "w")
            except IOError:
                print "\nThere were problems writing to %s\n" % filename
                traceback.print_exc(file = sys.stderr)
                raise
        else:
            self.f = tempfile.TemporaryFile()

    def generate(self):
        if not self.test:
            print "  Generating code..."
        self.__output_static_top_content()
        self.__output_compiler_defines()
        self.__output_thread_ids()
        self.__output_number_of_app_threads()
        self.__output_static_scheduler_macro()
        self.__output_port_ids()
        self.__output_number_of_ports()
        self.__output_mempools()
        self.__output_driver_constants()
        self.__output_includes_for_this_process()
        self.__output_static_bottom_content()
        if not self.test:
            self.f.close()
        else:
            self.f.seek(0)
            lines = self.f.readlines()
            self.f.close()
            return lines

    def __output_compiler_defines(self):
        defines = self.process.compiler.defines
        if defines:
            for define in defines:
                self.f.write("#define " + define + "\n")
        self.f.write("#include <bbos/compiler.h>\n\n")

    def __output_static_top_content(self):
        self.f.write(BBOS_H_TOP)

    def __output_thread_ids(self):
        self.f.write("/* Thread IDs */\n")
        for thread_id in range(0, len(self.threads)):
            self.f.write("#define " + self.threads[thread_id].upper() + " " + str(thread_id) + "\n")

    def __output_number_of_app_threads(self):
        self.f.write("\n/* The number of BBOS application threads */\n")
        self.f.write("#define BBOS_NUMBER_OF_APPLICATION_THREADS " + str(len(self.threads)) + "\n")

    def __output_static_scheduler_macro(self):
        if self.process.static_scheduler:
            # Add the the end of the list the implied threads
            if self.process.ipc:
                self.process.static_scheduler.append_thread(BBOS_IPC_THREAD_NAME)
            self.process.static_scheduler.append_thread(BBOS_IDLE_THREAD_NAME)

            # Output the static scheduler in the order defined by the user
            self.process.static_scheduler.output(self.f,
                                                 BBOS_STATIC_SCHEDULER_TOP,
                                                 BBOS_STATIC_SCHEDULER_BOTTOM)

    def __output_port_ids(self):
        if self.ports:
            self.f.write("\n/* Port IDs */\n")
            for port_id in range(0, len(self.ports)):
                self.f.write("#define " + self.ports[port_id] + " " + str(port_id) + "\n")

    def __output_number_of_ports(self):
        self.f.write("\n/* The number of ports in this process */\n")
        self.f.write("#define BBOS_NUMBER_OF_PORTS " + str(len(self.ports)) + "\n")

    def __output_mempools(self):
        if self.process.mempools:
            self.f.write("\n/* Mempool IDs */\n")
            for mempool_id in range(0, len(self.process.mempools)):
                self.f.write("#define " + self.process.mempools[mempool_id] + " " + str(mempool_id) + "\n")
            # Output the number of mempools in this process
            self.f.write("\n/* The number of mempools in this process */\n")
            self.f.write("#define BBOS_NUMBER_OF_MEMPOOLS " + str(len(self.process.mempools)) + "\n")

    def __output_driver_constants(self):
        if self.process.drivers:
            self.f.write("\n/* BBOS driver constants */\n")
            for driver in self.process.drivers:
                self.f.write("#define GPIO_DRIVER_NAME \"" + driver.name + "\"\n")
                self.f.write("#define GPIO_DRIVER_VERSION " + str(driver.version) + "\n")

    def __output_includes_for_this_process(self):
        include_files = self.process.get_include_files()
        if include_files:
            self.f.write("\n/* The include files we are using  */\n")
            for include in include_files:
                if include:
                    self.f.write("#include <" + include + ">\n")

    def __output_static_bottom_content(self):
        self.f.write(BBOS_H_BOTTOM)


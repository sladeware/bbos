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

BBOS_STATIC_SCHEDULER_TOP="""
/* Application static scheduler macro */
#define BBOS_SCHEDULER_STATIC
#define bbos_static_scheduler()  \\
  while(true) { \\
"""

BBOS_STATIC_SCHEDULER_BOTTOM="  }\n"


class GenerateCode:
    def __init__(self, config):
        self.config = config

        assert self.config[1].application, "You must define the application variable in bbos.py"

        assert len(self.config[1].application.processes) == 1, "Right now we can handle only one process."

        # The process we're genearting code for
        self.process = self.config[1].application.processes[0]

        # The list of threads within the process
        self.threads = self.process.threads + [d.name for d in self.process.drivers]

        # The list of main functions for each thread
        self.main_functions = self.process.threads + [d.main for d in self.process.drivers]

        # The list of ports
        self.ports = self.process.ports + [d.port for d in self.process.drivers]

        # Open the header file we're outputing to
        self.f = open(self.config[0] + "/bbos.h", "w")
        
    def generate(self):
        self.__output_static_top_content()
        self.__output_thread_ids()
        self.__output_number_of_app_threads()
        self.__output_static_scheduler_macro()
        self.__output_port_ids()
        self.__output_number_of_ports()
        self.__output_mempools()
        self.__output_driver_constants()
        self.__output_bootstrapper_functions()
        self.__output_exit_functions()
        self.__output_includes_for_this_process()
        self.__output_static_bottom_content()
        self.f.close()

    def __output_static_top_content(self):
        self.f.write(BBOS_H_TOP)

    def __output_thread_ids(self):
        self.f.write("/* Thread IDs */\n")
        for id in range(0, len(self.threads)):
            self.f.write("#define " + self.threads[id].upper() + " " + str(id) + "\n")

    def __output_number_of_app_threads(self):
        self.f.write("\n/* The number of BBOS application threads */\n")
        self.f.write("#define BBOS_NUMBER_OF_APPLICATION_THREADS " + str(len(self.threads)) + "\n")

    def __output_static_scheduler_macro(self):
        if self.process.static_scheduler:
            self.f.write(BBOS_STATIC_SCHEDULER_TOP)
            for main_function in self.main_functions:
                self.f.write("    " + main_function + "(); \\\n")
            self.f.write(BBOS_STATIC_SCHEDULER_BOTTOM)

    def __output_port_ids(self):
        self.f.write("\n/* Port IDs */\n")
        for id in range(0, len(self.ports)):
            self.f.write("#define " + self.ports[id] + " " + str(id) + "\n")

    def __output_number_of_ports(self):
        self.f.write("\n/* The number of ports in this process */\n")
        self.f.write("#define BBOS_NUMBER_OF_PORTS " + str(len(self.ports)) + "\n")

    def __output_mempools(self):
        self.f.write("\n/* Mempool IDs */\n")
        for id in range(0, len(self.process.mempools)):
            self.f.write("#define " + self.process.mempools[id] + " " + str(id) + "\n")
        # Output the number of mempools in this process
        self.f.write("\n/* The number of mempools in this process */\n")
        self.f.write("#define BBOS_NUMBER_OF_MEMPOOLS " + str(len(self.process.mempools)) + "\n")

    def __output_driver_constants(self):
        self.f.write("\n/* BBOS driver constants */\n")
        for driver in self.process.drivers:
            self.f.write("#define GPIO_DRIVER_NAME \"" + driver.name + "\"\n")
            self.f.write("#define GPIO_DRIVER_VERSION " + str(driver.version) + "\n")

    def __output_bootstrapper_functions(self):
        self.f.write("\n/* BBOS driver bootstrapper functions */\n")
        self.f.write("#define bbos_boot_drivers \\\n")
        for driver in self.process.drivers:
            self.f.write("    " + driver.boot + "(); \\\n")

    def __output_exit_functions(self):
        self.f.write("\n/* BBOS driver exit functions */\n")
        self.f.write("#define bbos_exit_drivers \\\n")
        for driver in self.process.drivers:
            self.f.write("    " + driver.exit + "(); \\\n")

    def __output_includes_for_this_process(self):
        self.f.write("\n/* The include files we are using  */\n")
        for include in self.process.get_include_files():
            self.f.write("#include <" + include + ">\n")

    def __output_static_bottom_content(self):
        self.f.write(BBOS_H_BOTTOM)


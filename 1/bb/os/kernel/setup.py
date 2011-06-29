#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

import os.path
import time
import module

from bb.builder.project import Wrapper
from bb.builder.compilers import CCompiler
from bb.os.kernel import Kernel, Hardware

def _gen_bbos_h(self, proj):
    # Generate the top of bbos.h file
    print "Generating:", proj.env['BBOS_H']
    f = open(proj.env['BBOS_H'], 'a')
    f.write("/*\n"
            " * %s\n"
            " *\n"
            " * This is BBOS generated source code used for late binding application\n"
            " * features just before compile time.\n"
            " *\n"
            " * Please do not edit this by hand, as your changes will be lost.\n"
            " *\n"
            " * %s\n"
            " */\n"
            % (time.asctime(), __copyright__))

    # Threads
    print "Number of threads: %d" % self.get_number_of_threads()
    f.write("/* Threads */\n")
    f.write("#define BBOS_NUMBER_OF_THREADS (%d)\n" 
            % self.get_number_of_threads())
    next_id = 0
        # Keep all thread entries. We will check all entry points and their 
        # aliases so they should not repeat
    entries = {}
    for thread in self.get_threads():
        assert not entries.has_key(thread.get_runner_name()), \
            "Thread '%s' has the same entry point as '%s'" \
            % (thread.get_name(), entries[thread.get_runner_name()].get_name())
        print "%20s : %4d" % (thread.get_name(), next_id)
        f.write("#define %s (%s)\n" % (thread.get_name(), next_id))
        # Register new entry point
        entries[thread.get_runner_name()] = thread
        next_id += 1
    # Commands
    print "Number of commands: %d" % self.get_number_of_commands()
    f.write("/* Commands */\n")
    f.write("#define BBOS_NUMBER_OF_COMMANDS (%d)\n" % self.get_number_of_commands())
    next_id = 0
    for command in self.get_commands():
        print "%20s : %4d" % (command.get_name(), next_id)
        f.write("#define %s (%s)\n" % (command.get_name(), next_id))
        next_id += 1   

    f.close()

    if not self.has_scheduler():
        exit(1)

AUTOGENERATED_FILES = {'BBOS_H': 'bbos.h'}

def _gen_files(proj):
    # Create files that have to be generated
    for (fid, fpath) in AUTOGENERATED_FILES.items():
        proj.env[fid] = os.path.join(proj.compiler.get_output_dir(), fpath)
        try:
            f = open(proj.env[fid], "w")
            #print "Create '%s' file" % proj.env[fid]
        except IOError:
            print "There were problems creating %s" % proj.env[fid]
            traceback.print_exc(file=sys.stderr)
            raise

@Wrapper.bind("on_build", Kernel)
def _build(kernel, project):
    _gen_files(project)
    _gen_bbos_h(kernel, project)

@Wrapper.bind("on_add", Kernel)
def _add_source(kernel, project):
    if isinstance(project.get_compiler(), CCompiler):
        project.get_compiler().add_include_dir(os.path.join(module.get_dir(), "../../.."))
        for filename in ("system.c", "thread.c", "idle.c"):
            project.add_source(module.get_file(__name__, filename))
    project.add_source(kernel.get_scheduler())
    project.add_source(kernel.get_hardware())

@Wrapper.bind("on_add", Hardware)
def _add_hardware(hardware, project):
    processor = hardware.get_processor()
    project.add_source(processor)
    

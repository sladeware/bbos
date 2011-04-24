
__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

import os
import sys
import traceback
from types import *

from bbos.kernel.thread import Thread
from bbos.kernel.message import Message
from bbos.kernel.idle import Idle
from bbos.component import Component

_default_messages = ["BBOS_DRIVER_INIT", "BBOS_DRIVER_OPEN", "BBOS_DRIVER_CLOSE"]

#______________________________________________________________________________

class Kernel(Component):
    """Kernel class."""
    def __init__(self, threads=[], messages=[]):
        Component.__init__(self, "Kernel")
        self.threads = {}
        self.messages = {}
        self.scheduler = None
        self.modules = {}
        self.add_messages(_default_messages)
        if len(threads):
            self.add_threads(threads)
        if len(messages):
            self.add_messages(messages)
    # __init__()

    def _attach(self, proj):
        """Generate the source code for the bbos.h header file used to late bind BBOS
        processes, threads and etc just before building. We need this since the
        C macro language is seriously underpowered for our purposes."""
        sources = [os.path.join(os.environ['BBOSHOME'], 'bbos/kernel/system.c'), 
                   os.path.join(os.environ['BBOSHOME'], 'bbos/kernel/port.c'),
                   os.path.join(os.environ['BBOSHOME'], 'bbos/kernel/thread.c')]
        proj.env['bbos.h'] = os.path.join(proj.compiler.get_output_dir(), "bbos.h")
        try:
            f = open(proj.env['bbos.h'], "a")
        except IOError:
            print "There were problems writing to %s" % "bbos.h"
            traceback.print_exc(file=sys.stderr)
            raise
        # Threads
        print "Process %d thread(s)" % self.get_number_of_threads()
        f.write("/* Threads */\n")
        f.write("#define BBOS_NUMBER_OF_THREADS (%d)\n" 
                % self.get_number_of_threads())
        next_id = 0
        # Keep all thread entries. We will check all entry points and their 
        # aliases so they should not repeat
        entries = {}
        for thread in self.threads.values():
            assert not entries.has_key(thread.get_entry()), \
                "Thread '%s' has the same entry point as '%s'" \
                % (thread.get_name(), entries[thread.get_entry()].get_name())
            print "%20s : %4d" % (thread.get_name(), next_id)
            f.write("#define %s (%s)\n" % (thread.get_name(), next_id))
            # Register new entry point
            entries[thread.get_entry()] = thread
            # Create aliases for entry functions only if they are different
            if thread.get_entry() != thread.get_alias():
                f.write("#define %s(...) %s(...)\n" % (thread.get_alias(), 
                        thread.get_entry()))
                # Register alias as a new entry point
                entries[thread.get_alias()] = thread
            next_id += 1
        # Messages
        print "Process %d message(s)" % self.get_number_of_messages()
        f.write("/* Messages */\n")
        f.write("#define BBOS_NUMBER_OF_MESSAGES (%d)\n" % self.get_number_of_messages())
        next_id = 0
        for message in self.messages.values():
            print "%20s : %4d" % (message.get_name(), next_id)
            f.write("#define %s (%s)\n" % (message.get_name(), next_id))
            next_id += 1
        if self.get_scheduler():
            f.write("/* Scheduling */\n")
            sources.append(self.get_scheduler())
        # Compile
        proj.add_sources(sources)
        proj.compiler.add_include_dirs([os.environ['BBOSHOME']])
    # config()

    def get_number_of_threads(self):
        return len(self.get_threads())

    def get_number_of_messages(self):
        return len(self.get_messages())
        
    def set_scheduler(self, sched):
        self.scheduler = sched
        self.add_thread(Idle())

    def get_scheduler(self):
        return self.scheduler

    def has_message(self, message):
        if type(message) == StringType:
            return self.messages.has_key(message)
        elif type(message) == InstanceType:
            if not isinstance(message, Message):
                print "Incorrect message instance: %s" % message
            return self.messages.has_key(message.get_name())

    def add_message(self, message):
        if type(message) == StringType:
            message = Message(message)
        if self.has_message(message):
            print "Message '%s' has been already added" % message.get_name()
            return
        self.messages[ message.get_name() ] = message
        return message

    def add_messages(self, messages):
        for message in messages:
            self.add_message(message)

    def get_message(self, message):
        if type(message) != StringType:
            return None
        if self.has_message(message):
            return self.messages[message]
        return None

    def get_messages(self):
        return self.messages.values()

    def has_thread(self, thread):
        if type(thread) == StringType:
            return self.threads.has_key(thread)
        elif type(thread) == InstanceType:
            if not isinstance(thread, Thread):
                print "Incorrect thread instance: %s" % thread
                return
            return self.threads.has_key(thread.get_name())

    def get_thread(self, thread):
        if type(thread) != StringType:
            return None
        if self.has_thread(thread):
            return self.threads[thread]
        return None

    def get_threads(self):
        return self.threads.values()

    def add_thread(self, thread):
        if self.has_thread(thread):
            print "Thread '%s' has been already added" % thread.get_name()
            return
        if type(thread) == StringType:
            thread = Thread(thread)
        self.threads[ thread.get_name() ] = thread
        return thread

    def add_threads(self, threads):
        for thread in threads:
            self.add_thread(thread)

    def add_module(self, mod_name):
        try:
            __import__(mod_name)
        except ImportError:
            traceback.print_exc(file=sys.stderr)
            raise
        mod = sys.modules[mod_name]
        mod_class_name = mod.__name__.split('.').pop().upper()
        try:
            mod_class = getattr(mod, mod_class_name)
        except AttributeError:
            print "Module %s should have class %s" % (mod_name, mod_class_name)
            raise
        mod_class_inst = mod_class(self)
        self.modules[mod_name] = mod_class_inst
        return mod_class_inst

    def get_module(self, module_name):
        pass

    def get_modules(self):
        return self.modules.values()

    def delete_module(self, module_name):
        pass


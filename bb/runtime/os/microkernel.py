#!/usr/bin/env python

__version__ = "0.1.0"

import types
import inspect

import bb
from bb import buildtime
from bb.runtime.thread import Thread

class Microkernel(object):
    class Exception(Exception):
        pass

    def __init__(self, microkernel):
        self._threads = dict()
        self.echo(self.banner())
        self.echo("Initialize microkernel")
        # Start initialization from the build-time microkernel
        self.register_threads(microkernel.get_threads())

    def start(self):
        self.test()
        self.echo("Start microkernel")

    def test(self):
        self.echo("Test microkernel")
        if not self.get_num_threads():
            raise Microkernel.Exception("At least one thread has to be added")

    def echo(self, data):
        if not isinstance(data, types.StringType):
            data = str(data)
        print data

    def register_threads(self, threads):
        for thread in threads:
            self.register_thread(thread)

    def register_thread(self, thread):
        if isinstance(thread, buildtime.Thread):
            thread = Thread(thread)
        elif not isinstance(thread, Thread):
            raise Exception()
        self.echo('Register thread "%s"' % thread.get_name())
        self._threads[thread.get_name()] = thread
        return thread

    def get_threads(self):
        return self._threads.values()

    def get_num_threads(self):
        return len(self.get_threads())

    def stop(self):
        """Shutdown everything and perform a clean system stop."""
        print "Microkernel stopped"
        sys.exit(0)

    def panic(self, text):
        """Halt the system.

        Display a message, then perform cleanups with stop. Concerning
        the application this allows to stop a single process, while
        all other processes are running.
        """
        lineno = inspect.getouterframes(inspect.currentframe())[2][2]
        fname = inspect.getmodule(inspect.stack()[2][0]).__file__
        self.echo("%s:%d:PANIC: %s" % (fname, lineno, text))
        # XXX we do not call stop() method here to do no stop the system twice.
        # exit() function will raise SystemExit exception, which will actually
        # call kernel's stop. See start() method for more information.
        self.stop()

    def banner(self):
        """Return nice BB OS banner."""
        return "BBOS Microkernel v" + __version__

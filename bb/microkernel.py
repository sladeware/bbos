#!/usr/bin/env python

import bb
from bb.build import packager

class Microkernel(object):
    def __init__(self):
        self._threads = dict()
        self._scheduler = None

    def get_threads(self):
        return self._threads.values()

    def get_num_threads(self):
        return len(self.get_threads())

    def unregister_thread(self, thread):
        if not isinstance(thread, bb.Thread):
            raise Exception()
        if thread.get_name() in self._threads:
            del self._threads[thread.get_name()]
        return thread

    def register_thread(self, thread):
        if not isinstance(thread, bb.Thread):
            raise Exception()
        self._threads[thread.get_name()] = thread
        return thread

    def register_threads(self, threads):
        for thread in threads:
            self.register_thread(thread)

@packager.pack(Microkernel, "simulator")
class _(packager.Package):
    FILES = ("./../runtime/microkernel.py",)

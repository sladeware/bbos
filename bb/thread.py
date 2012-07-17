#!/usr/bin/env python

class Thread(object):
    NAME = None
    RUNNER = None

    def __init__(self, name=None, runner=None):
        self._name = None
        self._runner = None
        if name:
            self.set_name(name)
        elif hasattr(self, "NAME"):
            self.set_name(getattr(self, "NAME"))
        if not self.get_name():
            raise Exception("Name wasn't provided")
        if runner:
            self.set_runner(runner)
        elif hasattr(self, "RUNNER"):
            self._runner = self.RUNNER

    def set_runner(self, runner):
        self._runner = runner

    def get_runner(self):
        return self._runner

    def set_name(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def __str__(self):
        return "Thread(%s)" % self.get_name()

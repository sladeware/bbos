#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

class Scheduler:
    """Provides the algorithms to select the threads for execution. 
    Interface for base scheduler class."""

    def move(self):
        """Decide who to run now."""
        raise NotImplemented

    def get_running_thread(self):
        raise NotImplemented

    def enqueue_thread(self, thread):
        raise NotImplemented

    def dequeue_thread(self, thread):
        raise NotImplemented


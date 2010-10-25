#!/usr/bin/python
# 
# Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
#
# This class builds the BBOS code, producing binary executables for the targets.
#


class BuildCode:
    def __init__(self, directory, application):
        processes = application.get_processes()

        # The process we're genearting code for
        assert len(processes) == 1, "Right now we can handle only one process."
        self.process = processes[0]

    def build(self):
        print "Building code..."

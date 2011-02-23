"""Quad core (dual processor / dual core) X86 simulation board.

A simulation of a no frills dual processor X86 system. Each processor
contains two X86 cores. The system supports POSIX and has a full glibc :)

This is very useful when you are prototyping and/or continuously testing
applications on a X86 system such as your desktop or laptop.
"""

__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

from bbos.hardware.board import Board
from bbos.hardware.processors import x86x2

class QuadX86SimulationBoard(Board):
    def __init__(self, processes):
        num_processes = len(processes)
        assert num_processes <= 4, "This quad core board cannot support %d processes" % num_processes

        processors = [x86x2(processes[0:1]), x86x2(processes[2:3])]
        Board.__init__(self, processors)



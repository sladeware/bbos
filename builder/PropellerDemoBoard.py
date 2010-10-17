# 
# Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
#

import BBOSBoard
from types import *

class PropellerDemoBoard(BBOSBoard.BBOSBoard):
    def __init__(self, process, amount_of_memory):
        BBOSBoard.BBOSBoard.__init__(self, process)

        self.amount_of_memory = amount_of_memory
        assert type(self.amount_of_memory) is IntType, "amount_of_memory is not an integer type: %d" % self.amount_of_memory
        assert self.amount_of_memory in (1, 5, 12), "amount_of_memory must be 1, 5 or 12: %d" % self.amount_of_memory

        # Modify includes
        self.process.append_include_files("propeller_demo_board.h")

        # Modify compiler include directories
        if self.process.compiler.includes:
            print "WARNING: Overwriting preexisting compiler include directories"
        self.process.compiler.includes = []

        # Modify compiler include argument
        if self.process.compiler.include_argument:
            print "WARNING: Overwriting preexisting compiler include argument"
        self.process.compiler.include_argument = "-I"

        # Modify compiler name
        if self.process.compiler.name:
            print "WARNING: Overwriting preexisting compiler name"
        self.process.compiler.name = "catalina"

        # Modify compiler options
        if self.process.compiler.options:
            print "WARNING: Overwriting preexisting compiler options"
        self.process.compiler.options = "-DDEMO -m " + str(self.amount_of_memory)

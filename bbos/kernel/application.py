"""Class representing a BBOS application, encapsulating a full system.

A BBOS application contains all the software and hardware resources of your
system. It is the highest level in the application hierachy. An application
contains boards, which are what your software runs on.
"""

__copyright__ = "Copyright (c) 2010 Slade Maurer, Alexander Sviridenko"

from bbos_board import *
from common import *


class BBOSApplication:
    def __init__(self, name, boards):
        # The name of this application
        self.name = verify_string(name)

        # The list of boards within this application
        self.boards = verify_list(boards)
        for board in self.boards:
            assert isinstance(board, BBOSBoard), "board is not a BBOSBoard: %s" % board

    def get_processes(self):
        processes = []
        for board in self.boards:
            processes += board.get_processes()
        return processes

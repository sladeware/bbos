"""Unit test for the BBOS board class
"""

__copyright__ = "Copyright (c) 2010 Slade Maurer, Alexander Sviridenko"

from bbos_board import *
from bbos_process import *
from bbos_processor import *
from bbos_core import *
import unittest

test_process = BBOSProcess(
    compiler=BBOSCompiler(),
    drivers=None,                         
    files=["finger.c"],
    ipc=True,
    mempools=[],
    ports=["FINGER_PORT"],
    static_scheduler=StaticScheduler(["move", "gpio_driver_main"]),
    threads=["move"]
)

CONTROL_THREADS=['move', 'bbos_idle', 'bbos_ipc']


class SanityCheck(unittest.TestCase):
    def testBoard(self):
        test_board = BBOSBoard([BBOSProcessor([BBOSCore(test_process)])])       
        self.assertEquals(CONTROL_THREADS, test_board.get_processes()[0].threads)

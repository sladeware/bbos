"""Unit test for the BBOS board class
"""

__copyright__ = "Copyright (c) 2010 Slade Maurer, Alexander Sviridenko"

from bbos.hardware.board import *
from bbos.hardware.core import *
from bbos.hardware.processor import *
from bbos.kernel.bbos_process import *
import unittest

test_process = BBOSProcess(
    compiler=BBOSCompiler(),
    drivers=None,                         
    files=["finger.c"],
    ipc=True,
    mempools=[],
    name="test_process",
    ports=["FINGER_PORT"],
    static_scheduler=StaticScheduler(["move", "gpio_driver_main"]),
    threads=["move"]
)

CONTROL_THREADS=['move', 'bbos_idle', 'bbos_ipc']


class SanityCheck(unittest.TestCase):
    def testBoard(self):
        test_board = BBOSBoard([BBOSProcessor([BBOSCore(test_process)])])       
        self.assertEquals(CONTROL_THREADS, test_board.get_processes()[0].threads)

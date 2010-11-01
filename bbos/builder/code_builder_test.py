"""Unit test for the BBOS code builder class.
"""

__copyright__ = "Copyright (c) 2010 Slade Maurer, Alexander Sviridenko"

from code_builder import *
from bbos.compiler import *
from bbos.hardware.boards.quad_x86_simulation_board import *
from bbos.hardware.driver import *
from bbos.kernel.bbos_process import *
import unittest

process0 = BBOSProcess(
    compiler=BBOSCompiler(),
    drivers=[],  
    files=["finger.c"],
    ipc=True,
    mempools=["FINGER_MEMPOOL"],
    name="process0",
    ports=["FINGER_PORT"],
    static_scheduler=None,
    threads=["move"]
)

quad_core_x86_simulation_board = QuadX86SimulationBoard(
    processes=[process0]
    )


class SanityCheck(unittest.TestCase):
    def testBuild(self):
        """Sanity test of BBOS code builder"""
        b = BuildCode(directory="",
                      process=process0,
                      test=True)
        self.assertEquals(len(control_lines), len(b.build()))

if __name__ == "__main__": 
    unittest.main()

control_lines = ['gcc -O -g -I. -I../.. -I/  -c -o /finger.o /finger.c', 'gcc -O -g -I. -I../.. -I/  -c -o /Users/slade/bbos/repo/bbos/trunk/bbos/builder/../bbos/kernel/time.o /Users/slade/bbos/repo/bbos/trunk/bbos/builder/../bbos/kernel/time.c', 'gcc -O -g -I. -I../.. -I/  -c -o /Users/slade/bbos/repo/bbos/trunk/bbos/builder/../bbos/kernel/process/port.o /Users/slade/bbos/repo/bbos/trunk/bbos/builder/../bbos/kernel/process/port.c', 'gcc -O -g -I. -I../.. -I/  -c -o /Users/slade/bbos/repo/bbos/trunk/bbos/builder/../bbos/kernel/process.o /Users/slade/bbos/repo/bbos/trunk/bbos/builder/../bbos/kernel/process.c', 'gcc -O -g -I. -I../.. -I/  -c -o /Users/slade/bbos/repo/bbos/trunk/bbos/builder/../bbos/kernel/system.o /Users/slade/bbos/repo/bbos/trunk/bbos/builder/../bbos/kernel/system.c', 'gcc -O -g -I. -I../.. -I/  -c -o /Users/slade/bbos/repo/bbos/trunk/bbos/builder/../bbos/kernel/mm/mempool.o /Users/slade/bbos/repo/bbos/trunk/bbos/builder/../bbos/kernel/mm/mempool.c', 'gcc -O -g -I. -I../.. -I/  -c -o /Users/slade/bbos/repo/bbos/trunk/bbos/builder/../bbos/kernel/process/thread.o /Users/slade/bbos/repo/bbos/trunk/bbos/builder/../bbos/kernel/process/thread.c', 'gcc -O -g -I. -I../.. -I/  -c -o /Users/slade/bbos/repo/bbos/trunk/bbos/builder/../bbos/kernel/process/thread/idle.o /Users/slade/bbos/repo/bbos/trunk/bbos/builder/../bbos/kernel/process/thread/idle.c', 'gcc -O -g -I. -I../.. -I/  -c -o /Users/slade/bbos/repo/bbos/trunk/bbos/builder/../bbos/kernel/hardware.o /Users/slade/bbos/repo/bbos/trunk/bbos/builder/../bbos/kernel/hardware.c', 'gcc -O -g -I. -I../.. -I/  -c -o bbos/kernel/process/scheduler/fcfs.o bbos/kernel/process/scheduler/fcfs.c', 'gcc -O -g -o /process0 /finger.o /Users/slade/bbos/repo/bbos/trunk/bbos/builder/../bbos/kernel/time.o /Users/slade/bbos/repo/bbos/trunk/bbos/builder/../bbos/kernel/process/port.o /Users/slade/bbos/repo/bbos/trunk/bbos/builder/../bbos/kernel/process.o /Users/slade/bbos/repo/bbos/trunk/bbos/builder/../bbos/kernel/system.o /Users/slade/bbos/repo/bbos/trunk/bbos/builder/../bbos/kernel/mm/mempool.o /Users/slade/bbos/repo/bbos/trunk/bbos/builder/../bbos/kernel/process/thread.o /Users/slade/bbos/repo/bbos/trunk/bbos/builder/../bbos/kernel/process/thread/idle.o /Users/slade/bbos/repo/bbos/trunk/bbos/builder/../bbos/kernel/hardware.o bbos/kernel/process/scheduler/fcfs.o ']





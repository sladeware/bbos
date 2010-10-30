"""Unit test for the BBOS code generator class.
"""

__copyright__ = "Copyright (c) 2010 Slade Maurer, Alexander Sviridenko"

from code_generator import *
from bbos.compiler import *
from bbos.hardware.driver import *
from bbos.kernel.bbos_process import *
import tempfile
import unittest

control_lines_top = ['\n',
                     '/*\n',
                     ' * This is BBOS generated source code used for late binding application\n',
                     ' * features just before compile time.\n',
                     ' *\n',
                     ' * Please do not edit this by hand, as your changes will be lost.\n',
                     ' *\n',
                     ' * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko\n',
                     ' */\n',
                     '\n',
                     '#ifndef __BBOS_H\n',
                     '#define __BBOS_H\n',
                     '\n',
                     '#include <bbos/compiler.h>\n',
                     '\n',
                     '/* Thread IDs */\n',
                     '#define MOVE 0\n',
                     '#define BBOS_IDLE 1\n',
                     '#define BBOS_IPC 2\n',
                     '#define GPIO 3\n',
                     '\n',
                     '/* The number of BBOS application threads */\n',
                     '#define BBOS_NUMBER_OF_APPLICATION_THREADS 4\n',
                     '\n']


control_lines_bottom = ['/* Port IDs */\n',
                        '#define FINGER_PORT 0\n',
                        '#define GPIO_DRIVER_PORT 1\n',
                        '\n',
                        '/* The number of ports in this process */\n',
                        '#define BBOS_NUMBER_OF_PORTS 2\n',
                        '\n',
                        '/* Mempool IDs */\n',
                        '#define FINGER_MEMPOOL 0\n',
                        '\n',
                        '/* The number of mempools in this process */\n',
                        '#define BBOS_NUMBER_OF_MEMPOOLS 1\n',
                        '\n',
                        '/* BBOS driver constants */\n',
                        '#define GPIO_DRIVER_NAME "gpio"\n',
                        '#define GPIO_DRIVER_VERSION 2\n',
                        '\n',
                        '#include <bbos/kernel.h>\n',
                        '\n',
                        '#endif /* __BBOS_H */\n']

static_control_lines = control_lines_top + ['/* Application static scheduler macro */\n',
                                            '#define BBOS_SCHEDULER_STATIC\n',
                                            '#define bbos_static_scheduler()  \\\n',
                                            '  while(true) { \\\n',
                                            '    move(); \\\n',
                                            '    gpio_driver_main(); \\\n', 
                                            '    bbos_ipc(); \\\n',
                                            '    bbos_idle(); \\\n',
                                            '  }\n',
                                            '\n'] + control_lines_bottom

fcfs_control_lines = control_lines_top + control_lines_bottom

gpio_driver = BBOSDriver(
    name="gpio",
    version=2,
    ports=["GPIO_DRIVER_PORT"],
    files=["/hardware/driver/gpio.c", "/hardware/driver/propeller.c"],
    )

fcfs_process = BBOSProcess(
    compiler=BBOSCompiler(),
    drivers=[gpio_driver],                         
    files=["finger.c"],
    ipc=True,
    mempools=["FINGER_MEMPOOL"],
    name="finger",
    ports=["FINGER_PORT"],
    static_scheduler=None,
    threads=["move"]
)

static_process = BBOSProcess(
    compiler=BBOSCompiler(),
    drivers=[gpio_driver],                         
    files=["finger.c"],
    ipc=True,
    mempools=["FINGER_MEMPOOL"],
    name="finger",
    ports=["FINGER_PORT"],
    static_scheduler=StaticScheduler(["move", "gpio_driver_main"]),
    threads=["move"]
)


class SanityCheck(unittest.TestCase):
    def testGenerateStaticScheduler(self):
        """Sanity test of BBOS code generation"""
        g = GenerateCode(directory="",
                         process=static_process,
                         test=True)
        self.compare_lines(static_control_lines, g.generate())

    def testGenerateFcfsScheduler(self):
        g = GenerateCode(directory="",
                         process=fcfs_process,
                         test=True)
        self.compare_lines(fcfs_control_lines, g.generate())

    def compare_lines(self, control_lines, test_lines):
        """Compare line by line to make debugging easier."""
        for control, test in zip(control_lines, test_lines):
            self.assertEquals(control, test)

if __name__ == "__main__": 
    unittest.main()

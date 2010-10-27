"""Unit test for the BBOS code generator class.
"""

__copyright__ = "Copyright (c) 2010 Slade Maurer, Alexander Sviridenko"

from bbos_code_generator import *
from bbos_compiler import *
from bbos_driver import *
from bbos_process import *
import tempfile
import unittest

verify_results = ['\n',
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
                  '\n',
                  '/* Application static scheduler macro */\n',
                  '#define BBOS_SCHEDULER_STATIC\n',
                  '#define bbos_static_scheduler()  \\\n',
                  '  while(true) { \\\n',
                  '    move(); \\\n',
                  '    bbos_idle(); \\\n',
                  '    bbos_ipc(); \\\n',
                  '    gpio_driver_main(); \\\n',
                  '  }\n',
                  '\n',
                  '/* Port IDs */\n',
                  '#define FINGER_PORT 0\n',
                  '#define GPIO_DRIVER_PORT 1\n',
                  '\n',
                  '/* The number of ports in this process */\n',
                  '#define BBOS_NUMBER_OF_PORTS 2\n',
                  '\n',
                  '/* Mempool IDs */\n',
                  '\n',
                  '/* The number of mempools in this process */\n',
                  '#define BBOS_NUMBER_OF_MEMPOOLS 0\n',
                  '\n',
                  '/* BBOS driver constants */\n',
                  '#define GPIO_DRIVER_NAME "gpio"\n',
                  '#define GPIO_DRIVER_VERSION 2\n',
                  '\n',
                  '/* BBOS driver bootstrapper functions */\n',
                  '#define bbos_boot_drivers \\\n',
                  '    gpio_driver_init(); \\\n',
                  '\n',
                  '/* BBOS driver exit functions */\n',
                  '#define bbos_exit_drivers \\\n',
                  '    gpio_driver_exit(); \\\n',
                  '\n',
                  '/* The include files we are using  */\n',
                  '\n',
                  '#include <bbos/kernel.h>\n',
                  '\n',
                  '#endif /* __BBOS_H */\n']

gpio_driver = BBOSDriver(
    name="gpio",
    version=2,
    ports=["GPIO_DRIVER_PORT"],
    boot="gpio_driver_init",
    main="gpio_driver_main",
    exit="gpio_driver_exit",
    files=["/hardware/driver/gpio.c", "/hardware/driver/propeller.c"],
    )

finger = BBOSProcess(
    compiler=BBOSCompiler(),
    drivers=[gpio_driver],                         
    files=["finger.c"],
    ipc=True,
    mempools=[],
    ports=["FINGER_PORT"],
    static_scheduler=True,
    threads=["move"]
)


class SanityCheck(unittest.TestCase):
    def testGenerate(self):
        """Sanity test of BBOS code generation"""
        g = GenerateCode(directory="",
                         process=finger,
                         test=True)

        # Compare line by line to make debugging easier
        for control, test in zip(verify_results, g.generate()):
            self.assertEquals(control, test)

if __name__ == "__main__": 
    unittest.main()

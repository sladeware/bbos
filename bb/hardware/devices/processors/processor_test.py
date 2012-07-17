#!/usr/bin/env python

import unittest

from bb.hardware.devices.processors import Processor

class ProcessorTest(unittest.TestCase):
    def setUp(self):
        pass

    def testCores(self):
        processor = Processor(2)
        self.assertEqual(processor.get_num_cores(), 2)

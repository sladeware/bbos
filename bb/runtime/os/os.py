#!/usr/bin/env python

import bb.runtime.os.microkernel as bb_kernel
from bb.runtime.autogen import bb_os_autogen

def init():
  bb_kernel.init()

def main():
  bb_autogen.thread_registration()

def start():
  bb_kernel.start()

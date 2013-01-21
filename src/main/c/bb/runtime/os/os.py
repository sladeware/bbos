#!/usr/bin/env python

import sys

import bb.runtime.os.config as bbos_config
import bb.runtime.os.microkernel as bbos_kernel
import bb.runtime.os.os_autogen

def init():
  bbos_kernel.init()

def main():
  thread_registration()

def start():
  bbos_kernel.start()

#!/usr/bin/env python

__version__ = "0.1.0"

import types
import inspect

import bb.runtime
import bb.runtime.os.config as bbos_config
from bb.runtime.os.config import bb_config

__all__ = ["bb_kernel_init", "bb_kernel_start", "bb_kernel_test",
           "bb_kernel_echo", "bb_kernel_register_thread", "bb_kernel_stop",
           "bb_kernel_panic", "bb_kernel_banner"]

_threads = list()

def init():
  echo(banner())
  echo("Initialize microkernel")
  echo("Supported number of threads: %d" % bb_config.BB_NR_THREADS)

def start():
  test()
  echo("Start microkernel")

def test():
  echo("Test microkernel")
  if not bb_config.BB_NR_THREADS:
    panic("At least one thread has to be added")

def echo(data):
  if not isinstance(data, types.StringType):
    data = str(data)
  print data

def register_thread(tid, runner):
  global _threads
  echo('Register thread "%d"' % tid)
  _threads[tid] = runner

def stop():
  """Shutdown everything and perform a clean system stop."""
  echo("Microkernel stopped")
  sys.exit(0)

def panic(text):
  """Halt the system.

  Display a message, then perform cleanups with stop. Concerning
  the application this allows to stop a single process, while
  all other processes are running.
  """
  lineno = inspect.getouterframes(inspect.currentframe())[2][2]
  fname = inspect.getmodule(inspect.stack()[2][0]).__file__
  echo("%s:%d:PANIC: %s" % (fname, lineno, text))
  # XXX we do not call stop() method here to do no stop the system twice.
  # exit() function will raise SystemExit exception, which will actually
  # call kernel's stop. See start() method for more information.
  stop()

def banner():
  """Return nice BB OS banner."""
  return "BBOS Microkernel v" + __version__

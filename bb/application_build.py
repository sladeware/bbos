#!/usr/bin/env python
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'
__author__ = 'Oleksandr Sviridenko'

"""Application build-file."""

import sys

import bb

class SingleKernelOS(bb.builder.Image):
  """This image class supports one OS per binary."""

class MultiKernelOS(bb.builder.Image):
  """This image class supports multiple OS'es inside of result binary."""

  def __init__(self, mapping, processor, thread_distribution):
    bb.builder.Image.__init__(self)
    self._mapping = mapping
    os_class = mapping.get_os_class()
    print ' ', str(processor)
    self.add_target(processor)
    for core, threads in thread_distribution[processor].items():
      # Skip the core if we do not have a threads for it
      if not threads:
        continue
      print '  ', str(core), ':', [str(_) for _ in threads]
      os = os_class(core=core, threads=threads)
      self.add_targets([os, os.get_kernel(),
                        os.kernel.get_scheduler()])
      self.add_targets(os.kernel.get_threads())

  def get_name(self):
    return '%s' % (self._mapping.get_name(),)

class Application(bb.builder.Application):

  def build_images(self):
    print 'Analyse application'
    mappings = bb.application.get_mappings()
    for mapping in mappings:
      print 'Analyse mapping "%s"' % mapping.get_name()
      if not mapping.get_num_threads():
        logging.error("Mapping", mapping.get_name(), "doesn't have threads")
        sys.exit(1)
      print "*", "number of threads", "=", mapping.get_num_threads()
      board = mapping.get_board()
      if not board:
        print "Mapping", mapping.get_name(), "doesn't connected to a board"
        sys.exit(1)
      thread_distributor = mapping.get_thread_distributor()
      print "*", "board", "=", str(board)
      if not board.get_processors():
        print "Board doesn't have any processors"
        sys.exit(1)
      print "Thread distribution:"
      thread_distribution = thread_distributor(mapping.get_threads(),
                                               board.get_processors())
      for processor in board.get_processors():
        # TODO(team): replace this later with a flag and provide an apportunity
        # to use SingleOSImage class.
        self.add_image(MultiKernelOS(mapping, processor, thread_distribution))

#  def extract_os_targets(self, os):
#    """Basically this is a wrapper for add_component()."""
#    return (os, os.kernel, os.kernel.get_threads(), os.kernel.get_scheduler(),
#            os.core.get_processor())

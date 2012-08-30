#!/usr/bin/env python

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'
__author__ = 'Oleksandr Sviridenko'

import bb
from bb.os.messenger import Messenger
from bb.tools.generators import CGenerator

def gen_runner_c(messenger):
  file_path = bb.host_os.path.join(messenger.get_runner() + '_autogen.c')
  g = CGenerator().create(file_path)
  g.writeln('void %s()' % messenger.get_runner())
  g.writeln('{')
  g.writeln('}')
  g.close()
  return file_path

with Messenger as target:
  target.build_cases.update({
      'propeller': {
        'sources': (gen_runner_c,)
        }
      })

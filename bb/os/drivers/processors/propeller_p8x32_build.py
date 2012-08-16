#!/usr/bin/env python

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'
__author__ = 'Oleksandr Sviridenko'

import os

import bb
from bb import Builder
from bb.hardware.devices.processors import PropellerP8X32A

def update_bbos_config_h(processor):
  file_path = os.path.join(bb.env['BB_HOME'], 'bb', 'os', 'config_autogen.h')
  fh = open(file_path, 'a')
  fh.write("#define BBOS_CONFIG_PROCESSOR propeller_p8x32\n")
  fh.close()

def gen_main_c(processor):
  file_path = os.path.join(bb.env.pwd(), 'propeller_p8x32', 'main_autogen.c')
  fh = open(file_path, 'w')
  fh.write('#include "main_autogen.h"\n')
  fh.write('\n')
  fh.write('int main()\n')
  fh.write('{\n')

  for core in processor.get_cores():
    if not core.get_os():
      continue
    fh.write('  main%d();\n' % core.get_id());

  fh.write('}\n')
  fh.close()
  return file_path

def gen_main_h(processor):
  file_path = os.path.join(bb.env.pwd(), 'propeller_p8x32', 'main_autogen.h')
  fh = open(file_path, 'w')
  fh.write('#ifndef __MAIN_AUTOGEN_H\n')
  fh.write('#define __MAIN_AUTOGEN_H\n')

  for core in processor.get_cores():
    if not core.get_os():
      continue
    fh.write('void main%d();\n' % core.get_id());

  fh.write('#endif /* __MAIN_AUTOGEN_H */\n')
  fh.close()

Builder.rule(PropellerP8X32A, {
    'PropellerToolchain' : {
      'srcs': (gen_main_c, gen_main_h,
               update_bbos_config_h,
               "propeller_p8x32/cog.c", "propeller_p8x32/delay.c")
      }
})

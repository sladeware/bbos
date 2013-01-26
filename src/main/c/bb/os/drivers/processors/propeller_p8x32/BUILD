# -*- endoing: utf-8; mode: python; -*-
#
# http://www.bionicbunny.org/
# Copyright (c) 2012-2013 Sladeware LLC
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
#
# Author: Oleksandr Sviridenko

from django.template import Template, Context

import bb
from bb.utils.func import partials
from bb.host_os.path import join, touch, dirname, exists
from bb.app.os import OS
from bb.hardware.devices.processors.propeller_p8x32 import PropellerP8X32A

def update_config_h(os, compiler_params):
  input_file = join(bb.get_app().get_build_dir(), "bb", "os", "config_autogen.h")
  if not exists(input_file):
    raise Exception("%s cannot be found" % input_file)
  with open(input_file, "a") as fh:
    fh.write("#define BBOS_CONFIG_PROCESSOR propeller_p8x32\n")

def gen_main_c(os, compiler_params):
  """Generates ``bb/os/main_autogen.c`` file."""
  template = None
  input_file = join(dirname(__file__), "main_autogen.c.in")
  with open(input_file) as fh:
    template = Template(fh.read())
    ctx = Context(
      {
        "kernels": os.get_kernels(),
        # TODO(team): the stack size has to be consider for each thread
        # individually
        "stack_size": 16,
        "copyright": __copyright__,
      }
    )
  output_file = touch([bb.get_app().get_build_dir(), "bb", "os",
                       "main_autogen.c"], recursive=True)
  with open(output_file, "w") as fh:
    fh.write(template.render(ctx))
  return output_file

def gen_main_h(os, compiler_params):
  template = None
  input_file = join(dirname(__file__), "main_autogen.h.in")
  with open(input_file) as fh:
    template = Template(fh.read())
  output_file = join(bb.get_app().get_build_dir(), "bb", "os", "main_autogen.h")
  with open(output_file, "w") as fh:
    context = Context({
      "os": os,
      "copyright": __copyright__,
    })
    fh.write(template.render(context))

os_builder = bb.get_bldr(OS)
os_builder.read_compiler_params(
  {
    "propgcc": {
      "sources": partials((gen_main_c, gen_main_h, update_config_h,)), os
    }
  }
)

propeller_builder = bb.get_bldr(PropellerP8X32A)
propeller_builder.read_compiler_params({
  "propgcc": {
      "sources": ("core.c", "delay.c", "sio.c",)
  }
})

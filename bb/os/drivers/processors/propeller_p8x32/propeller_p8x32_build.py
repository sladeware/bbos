#!/usr/bin/env python
#
# http://bionicbunny.org/
# Copyright (c) 2012 Sladeware LLC
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

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

from django.template import Template, Context

import bb
from bb import host_os
from bb.app.os import OS
from bb.hardware.devices.processors.propeller_p8x32 import PropellerP8X32A
from bb.tools.generators import CGenerator

os_builder = bb.get_bldr(OS)

@os_builder
def update_config_h(os):
  in_ = host_os.path.join(bb.get_app().get_build_dir(), "bb", "os",
                          "config_autogen.h")
  if not host_os.path.exists(in_):
    raise Exception("%s cannot be found" % in_)
  with open(in_, "a") as fh:
    fh.write("#define BBOS_CONFIG_PROCESSOR propeller_p8x32\n")

@os_builder
def gen_main_c(os):
  """Generates ``bb/os/main_autogen.c`` file."""
  in_ = host_os.path.join(host_os.path.dirname(__file__), "main_autogen.c.in")
  template = None
  with open(in_) as fh:
    template = Template(fh.read())
    ctx = Context({
      "kernels": os.get_kernels(),
      # TODO(team): the stack size has to be consider for each thread
      # individually
      "stack_size": 16,
      "copyright": __copyright__,
    })
  out = host_os.path.touch([bb.get_app().get_build_dir(), "bb", "os",
                            "main_autogen.c"], recursive=True)
  with open(out, "w") as fh:
    fh.write(template.render(ctx))
  return out

@os_builder
def gen_main_h(os):
  app = bb.get_app()
  path = host_os.path.join(bb.get_app().get_build_dir(), "bb", "os",
                           "main_autogen.h")
  g = CGenerator().create(path)
  for kernel in os.get_kernels():
    core = kernel.get_core()
    g.writeln("void main%d(void* arg);" % core.get_id());
  g.close()

os_builder.read_compiler_params({
    "propgcc": {
      "sources": (gen_main_c, gen_main_h, update_config_h,)
    }
})

builder = bb.get_bldr(PropellerP8X32A)
builder.read_compiler_params({
    "propgcc": {
      "sources": ("core.c", "delay.c", "sio.c",)
    }
})

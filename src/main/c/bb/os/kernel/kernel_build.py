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
from bb.app.os.kernel.schedulers import StaticScheduler
from bb.tools.generators import CGenerator

kernel_builder = bb.get_bldr(bb.os.Kernel)

@kernel_builder
def gen_main_c(kernel):
  core = kernel.get_core()
  if not core:
    raise Exception("Core wasn't assigned to the the kernel!")
  out = host_os.path.touch([bb.get_app().get_build_dir(), "bb", "os",
                            "main%d_autogen.c" % core.id], recursive=True)
  in_ = host_os.path.join(host_os.path.dirname(__file__), "main_autogen.c.in")
  with open(in_) as fh:
    template = Template(fh.read())
    ctx = Context({
      "core": core,
      "threads": kernel.get_threads(),
    })
    g = CGenerator(out, "w")
    g.write(template.render(ctx))
    g.close()
  return out

@kernel_builder
def update_config_h(kernel):
  app = bb.get_app()
  h = host_os.path.join(app.get_build_dir(), "bb", "os", "config_autogen.h")
  g = CGenerator(h, "a")
  # Add prototypes of runner functions
  for thread in kernel.get_threads():
    g.writeln("void %s();" % thread.runner)
  g.close()

kernel_builder.read_compiler_params(
  {
    "propgcc": {
      "sources": (gen_main_c, update_config_h, "../kernel.c")
     }
  }
)

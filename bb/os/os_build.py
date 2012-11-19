#!/usr/bin/env python
#
# http://www.bionicbunny.org/
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

os_builder = bb.get_bldr(OS)

@os_builder
def gen_os_c(os):
  """Generates `bb/os_autogen.c` and returns its name."""
  ports = [_.get_port() for _ in \
             filter(lambda thread: thread.has_port(),
                    sorted(os.get_threads(),
                           key=lambda thread: thread.has_port(),
                           reverse=True))]
  template = None
  in_ = host_os.path.join(host_os.path.dirname(__file__), "os_autogen.c.in")
  with open(in_) as fh:
    template = Template(fh.read())
  out = host_os.path.touch([bb.get_app().get_build_dir(), "bb", "os_autogen.c"],
                           recursive=True)
  with open(out, "w") as fh:
    context = Context({
      "ports": ports,
      "copyright": __copyright__,
    })
    fh.write(template.render(context))
  return out

@os_builder
def gen_config_h(os):
  """Generates `bb/os/config_autogen.h` header filem which will be included by
  `bb/os/config.h` header file.
  """
  template = None
  in_ = host_os.path.join(host_os.path.dirname(__file__), "config_autogen.h.in")
  with open(in_) as fh:
    template = Template(fh.read())
  out = host_os.path.touch([bb.get_app().get_build_dir(), "bb", "os",
                            "config_autogen.h"], recursive=True)
  with open(out, "w") as fh:
    context = Context({
      "BBOS_NUM_THREADS": os.get_num_threads(),
      "BBOS_NUM_PORTS": sum([thread.has_port() for thread in os.get_threads()]),
      "BBOS_MAX_MESSAGE_PAYLOAD_SIZE": 2,
      "BBOS_NUM_KERNELS": os.get_num_kernels(),
      "sorted_threads": sorted(os.get_threads(),
                               key=lambda thread: thread.has_port(),
                               reverse=True),
      "messages": os.get_messages(),
      "copyright": __copyright__,
    })
    fh.write(template.render(context))

os_builder.read_compiler_params(
  {
    "propgcc": {
      "sources": (
        "../os.c", "port.c", "mm/mempool.c",
        gen_os_c,
        gen_config_h,
      )
    }
  }
)

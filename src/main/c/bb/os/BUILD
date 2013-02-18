# -*- coding: utf-8; mode: python; -*-
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

from bb import __copyright__
from bb.app.meta_os import OS
from bb.utils.path_utils import localpath
from bb.utils import logging

logger = logging.get_logger("bb")

def gen_runner_h(msngr):
  """Generates runner's header file. The file will be stored in the same
  directory, where the build file is located or in the current directory.
  """
  input_fn = path_utils.localpath("messenger_autogen.h.in")
  output_fn = self.buildpath(["bb", "os", "%s_autogen.h" %
                              msngr.get_runner()])
  with open(input_fn) as in_fh, open(output_fn, "w") as output_fh:
    template = Template(input_fh.read())
    context = Context({
      "messenger": msngr,
      "copyright": __copyright__
    })
    view = template.render(context)
    output_fh.write(view)

def gen_runner_c(rule, msngr, files):
  """Generates messenger runner `runner_autogen.c` from messenger_autogen.c.in
  template file.
  """
  if not typecheck.is_list(files):
    raise TypeError()
  output_fn = self.buildpath(["bb", "os", "%s_autogen.c" % msngr.get_runner()])
  input_fn = path_utils.localpath("messenger_autogen.c.in")
  with open(input_fn) as input_fh, open(output_fn, "w") as output_fh:
    template = Template(input_fh.read())
    context = Context({
      "messenger": msngr,
      "copyright": __copyright__,
      "message_handlers_files": files
    })
    view = template.render(context)
    output_fh.write(view)
  return output_fn

def gen_os_c(rule, os):
  """Generates `bb/os_autogen.c` and returns its name."""
  ports = [_.get_port() for _ in \
             filter(lambda thread: thread.has_port(),
                    sorted(os.get_threads(),
                           key=lambda thread: thread.has_port(),
                           reverse=True))]
  input_fn = localpath("os_autogen.c.in")
  output_fn = rule.buildpath(["bb", "os_autogen.c"])
  with open(input_fn) as input_fh, open(output_fn, "w") as output_fh:
    template = Template(input_fh.read())
    context = Context({
        "ports": ports,
        "copyright": __copyright__,
    })
    output_fh.write(template.render(context))
  return [output_fn]

def gen_config_h(rule, os):
  """Generates `bb/os/config_autogen.h` header file, which will be automatically
  included by `bb/os/config.h` header file.
  """
  input_fn = localpath("config_autogen.h.in")
  output_fn = rule.buildpath(["bb", "os", "config_autogen.h"])
  with open(input_fn) as input_fh, open(output_fn, "w") as output_fh:
    template = Template(input_fh.read())
    context = Context({
      "BBOS_CONFIG_PROCESSOR": os.get_processor().properties.family,
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
    output_fh.write(template.render(context))
    # Add prototypes of thread runners
    for kernel in os.get_kernels():
      for thread in kernel.get_threads():
        output_fh.write("void %s();\n" % thread.get_runner())

def gen_main_c(rule, os):
  result_outputs = []
  for kernel in os.get_kernels():
    core = kernel.get_core()
    if not core:
      raise Exception("Core wasn't assigned to the the kernel!")
    input_fn = localpath("kernel/main_autogen.c.in")
    output_fn = rule.buildpath(["bb", "os", "main%d_autogen.c" % core.id])
    with open(input_fn) as input_fh, open(output_fn, "w") as output_fh:
      template = Template(input_fh.read())
      context = Context({
        "core": core,
        "threads": kernel.get_threads(),
      })
      output_fh.write(template.render(context))
    result_outputs.append(output_fn)
  return result_outputs

def gen_main_h(rule, os):
  input_fn = localpath("main_autogen.h.in")
  output_fn = rule.buildpath(["bb", "os", "main_autogen.h"])
  with open(input_fn) as input_fh, open(output_fn, "w") as output_fh:
    template = Template(input_fh.read())
    context = Context({
      "os": os,
      "copyright": __copyright__,
    })
    output_fh.write(template.render(context))

cc_library_factory(target = OS,
                   srcs = ["../os.c", "port.c", "mm/mempool.c",
                           gen_os_c, gen_config_h, gen_main_h,
                           gen_main_c],
                   # TODO: the following includes have to be fixed. This is
                   # temporary solution to include main/c directory.
                   includes = [localpath("../..")])

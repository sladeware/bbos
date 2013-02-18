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
from bb.app.hardware.devices.processors.propeller_p8x32 import PropellerP8X32A
from bb.utils.path_utils import localpath, exists

def update_config_h(rule, os):
  input_fn = rule.buildpath(["bb", "os", "config_autogen.h"])
  if not exists(input_fn):
    raise OSError("%s cannot be found" % input_file)
  with open(input_fn, "a") as input_fh:
    input_fh.write("#define BBOS_CONFIG_PROCESSOR propeller_p8x32\n")

def gen_main_c(rule, os):
  """Generates ``bb/os/main_autogen.c`` file."""
  input_fn = localpath("main_autogen.c.in")
  output_fn = rule.buildpath(["bb", "os", "main_autogen.c"])
  with open(input_fn) as input_fh, open(output_fn, "w") as output_fh:
    template = Template(input_fh.read())
    context = Context({
      "kernels": os.get_kernels(),
      # TODO(team): the stack size has to be consider for each thread
      # individually
      "stack_size": 16,
      "copyright": __copyright__,
    })
    output_fh.write(template.render(context))
  return output_fn


cc_library_factory(target = OS,
                   srcs = [gen_main_c, update_config_h],
                   # TODO: the following includes have to be fixed. This is
                   # temporary solution to include main/c directory.
                   includes = [localpath("../../../../../")])

cc_library_factory(target = PropellerP8X32A,
                   srcs = ["core.c", "delay.c", "sio.c"])

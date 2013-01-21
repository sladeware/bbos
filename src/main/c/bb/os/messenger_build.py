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

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

from django.template import Template, Context

import bb
from bb.utils.func import partials
from bb.host_os.path import join, touch, dirname

messenger_builder = bb.get_builder(bb.os.Messenger)

@messenger_builder.trigger
def gen_runner_h(builder, compiler_params):
  """Generates runner's header file. The file will be stored in the
  same directory, where the build file is located or in the current
  directory.
  """
  template = None
  input_file = join(dirname(__file__), "messenger_autogen.h.in")
  with open(input_file) as fh:
    template = Template(fh.read())
  output_file = touch([bb.get_app().get_build_dir(), "bb", "os",
                       "%s_autogen.h" % messenger.get_runner()], recursive=True)
  with open(output_file, "w") as fh:
    context = Context(
      {
        "messenger": messenger,
        "copyright": __copyright__,
      }
    )
    fh.write(template.render(context))

@messenger_builder.trigger
def gen_runner_c(builder, compiler_params):
  # Read template
  template = None
  input_file = join(dirname(__file__), "messenger_autogen.c.in")
  with open(input_file) as fh:
    template = Template(fh.read())
  # Render template and generate output file
  output_file = touch([bb.get_app().get_build_dir(), "bb", "os",
                       "%s_autogen.c" % messenger.get_runner()], recursive=True)
  with open(output_file, "w") as fh:
    context = Context(
      {
        "messenger": messenger,
        "copyright": __copyright__,
      }
    )
    fh.write(template.render(context))
  return output_file

@messenger_builder.trigger
def incapsulate(builder, compiler_params, files):
  return files

class MessengerBuild(Build):
  OBJECT = bb.os.Messenger
  COMPILER_PARAMS = {
    "propgcc": {
      "sources": (gen_runner_c, gen_runner_h),
    }
  }

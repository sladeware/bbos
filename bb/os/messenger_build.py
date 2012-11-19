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

import inspect
from django.template import Template, Context

import bb
from bb import host_os

msngr_builder = bb.get_bldr(bb.os.Messenger)

@msngr_builder
def gen_runner_h(messenger):
  """Generates runner's header file. The file will be stored in the
  same directory, where the build file is located or in the current
  directory.
  """
  template = None
  in_ = host_os.path.join(host_os.path.dirname(__file__),
                          "messenger_autogen.h.in")
  with open(in_) as fh:
    template = Template(fh.read())
  out = host_os.path.touch([bb.get_app().get_build_dir(), "bb", "os",
                            "%s_autogen.h" % messenger.get_runner()],
                           recursive=True)
  with open(out, "w") as fh:
    context = Context({
      "messenger": messenger,
      "copyright": __copyright__,
    })
    fh.write(template.render(context))

@msngr_builder
def gen_runner_c(messenger):
  template = None
  in_ = host_os.path.join(host_os.path.dirname(__file__),
                          "messenger_autogen.c.in")
  with open(in_) as fh:
    template = Template(fh.read())
  out = host_os.path.touch([bb.get_app().get_build_dir(), "bb", "os",
                            "%s_autogen.c" % messenger.get_runner()],
                           recursive=True)
  with open(out, "w") as fh:
    context = Context({
      "messenger": messenger,
      "copyright": __copyright__,
    })
    fh.write(template.render(context))
  return out

msngr_builder.read_compiler_params(
  {
    "propgcc": {
      "sources": (gen_runner_c, gen_runner_h),
    }
  }
)

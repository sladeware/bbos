#!/usr/bin/env python
#
# http://bionicbunny.org/
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

import types

import bb

# NOTE: I used to use meta-class, which makes creating of builder much more
# efficient. However there is a problems with dependencies.

class Object(bb.Object, bb.Object.Cloneable):
  """This object class is derived from :class:`bb.object.Object` and has to be
  used as a basis for any application object.
  """

  def __init__(self):
    bb.Object.__init__(self)

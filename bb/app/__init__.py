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

"""Contains high-level classes encapsulating the overall BB application
model.

BB application combines all of the build systems of all of the defined
processes. Therefore the application includes the models of processes, their
communication, hardware description, simulation and build specifications. At the
same time the processes inside of an application can be segmented into
`clusters`, or a group of CPUs.
"""

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

from bb.app.app import Application
from bb.app.object import Object
from bb.app.mapping import Mapping, mapping_class_factory
from bb.app.shell import Shell

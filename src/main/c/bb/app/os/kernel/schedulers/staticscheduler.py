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

from bb.app.os.kernel.schedulers.scheduler import Scheduler

class StaticScheduler(Scheduler):
  """Static scheduling is widely used with dependable real-time systems in
  application areas such as aerospace and military systems, automotive
  applications, etc.

  In static scheduling, scheduling are made during compile time. This assumes
  parameters of all the tasks is known a priori and builds a schedule based on
  this. Once a schedule is made, it cannot be modified online. Static scheduling
  is generally not recommended for dynamic systems (use dynamic scheduler
  instead).
  """

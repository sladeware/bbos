#!/usr/bin/env python
#
# http://www.bionicbunny.org/
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

from __future__ import print_function

print("BBOS SETUP")
print()

# Skip bbapp automatic installation for now

import bb
from bb.utils import path_utils

location = path_utils.dirname(path_utils.realpath(__file__))
print("Update user config")
bb.user_config.set("bbos", "location", location)
bb.user_config.write()

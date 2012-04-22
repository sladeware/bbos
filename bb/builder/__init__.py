#!/usr/bin/env python

"""The BB Builder (simply builder or BBB) provides an environment for
application development. It allows the application developer to map
software to computational resources and is a a key part of Bionic
Bunny."""

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__copyright__ = "Copyright (c) 2012 Sladeware LLC"

from bb.builder.configs import Config

_config = Config()

def get_config():
    return _config
    

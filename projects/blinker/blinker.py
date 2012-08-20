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

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'

import bb
from bb.hardware.devices.boards import P8X32A_QuickStartBoard

blinker = bb.Mapping('Blinker', board=P8X32A_QuickStartBoard())
blinker.register_threads([bb.os.Thread('B0', 'b0_runner'),
                          bb.os.Thread('B1', 'b1_runner')])

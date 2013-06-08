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

"""A BBOS driver is typical for a microkernel in that it uses messaging for
communication with other parts of the system. Asynchronous and synchronous
events are handled within the driver, with notification sent as required to
waiting threads.

A :class:`Driver` is extended version of
:class:`~bb.app.os.messenger.Messenger`. This messenger demultiplexes
messages into commands/payload and passes them to the driver core. It bundles
commands/payloads and sends to the thread requested by the driver core.
"""

from bb.app.os.messenger import Messenger

class Driver(Messenger):
  """This class represents a driver."""

  name_format = "DRIVER_%d"

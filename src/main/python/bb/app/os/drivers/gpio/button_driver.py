# -*- coding: utf-8; -*-
#
# Copyright (c) 2012-2013 Sladeware LLC
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
#
# Author: Oleksandr Sviridenko

"""The button driver tracks pressed buttons.

The following table describes messages and their handlers supported by the
button driver:

====================  =======================  ==============
Action                Message ID               Message Fields
====================  =======================  ==============
is_button_pressed     **IS_BUTTON_PRESSED**    pin (1 byte)
are_buttons_pressed   **ARE_BUTTONS_PRESSED**  mask (4 bytes)
====================  =======================  ==============

Small example. Suppose you have a button driver ``BUTTON_DRIVER``. The following
code snippet shows how to write a simple C runner template ``my_runner`` that
will check for active buttons:

.. code-block:: c
   :linenos:
   :emphasize-lines: 9, 10, 18

   #include "bb/os.h"

   void
   my_runner()
   {
     struct bbos_message* msg;
     uint16_t mask;
     if ((msg = bbos_receive_message()) != NULL) {
       if (msg->label == ARE_BUTTONS_PRESSED) {
         mask = *((uint16_t*)msg->payload);
         /* Do something with active buttons... */
       }
       bbos_delete_message(msg);
       return;
     }
     /* Request buttons bits */
     if ((msg = bbos_request_message(BUTTON_DRIVER)) != NULL) {
       msg->label = ARE_BUTTONS_PRESSED;
       *((uint16_t*)msg->payload) = 0xFF;
       bbos_send_message(msg);
     }
   }

Lines 9 and 18 shows how to receive and send ``ARE_BUTTONS_PRESSED`` message
respectively. Line 10 shows how to read a mask of pressed buttons.

"""

from bb.app.os import Driver

class ButtonDriver(Driver):
  """This class represents button driver."""

  name_format = "BUTTON_DRIVER_%d"
  runner = "button_driver_runner"
  message_handlers = [
    ('is_button_pressed',
     ('IS_BUTTON_PRESSED', [('pin', 1)]),
     ('PRESSED_BUTTON', [('pin', 1)])),
    ('are_buttons_pressed',
     ('ARE_BUTTONS_PRESSED', [('mask', 4)]),
     ('PRESSED_BUTTONS', [('mask', 4)])),
  ]

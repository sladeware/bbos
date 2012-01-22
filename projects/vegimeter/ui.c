/* Copyright 2011 Sladeware LLC
 *
 *   Licensed under the Apache License, Version 2.0 (the "License");
 *   you may not use this file except in compliance with the License.
 *   You may obtain a copy of the License at
 *
 *       http://www.apache.org/licenses/LICENSE-2.0
 *
 *   Unless required by applicable law or agreed to in writing, software
 *   distributed under the License is distributed on an "AS IS" BASIS,
 *   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *   See the License for the specific language governing permissions and
 *   limitations under the License.
 */

#include <bb/os/drivers/gpio/button.h>

void ui_runner() {
  unsigned button_mask = 0xFFUL;
  unsigned mask, i;

  do {
    mask = are_buttons_pressed(button_mask);
    if(mask) {
      for (i = 0; i < 8; i++, mask >>= 1) {
	if (mask & 1UL) {
	  printf("Button : %d\n", i);
	}
      }
    }
  } while (1);
}

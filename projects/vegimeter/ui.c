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
#include <bb/os/drivers/gpio/lh1500.h>

void ui_runner() {
  uint8_t button_pin = 0;
  uint8_t lh1500_pin = 13;
  uint8_t on = 0;

  do {
    if(is_button_pressed(button_pin) > 0) {
      printf("Button pressed!\n");
      if(on == 0) {
	lh1500_on(lh1500_pin);
	on = 1;
      } else {
	lh1500_off(lh1500_pin);
	on = 0;
      }
    }
  } while (1);
}

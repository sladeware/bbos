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
#include <vegimeter.h>

void button_driver_runner() {
  unsigned button_mask = 0xFFUL; /* QuickStart board has P0 - P7 as buttons */
  unsigned mask, i;

  vegimeter_buttons |= are_buttons_pressed(button_mask);
}

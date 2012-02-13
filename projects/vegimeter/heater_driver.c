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

#include <vegimeter.h>

void heater_driver_runner() {
  if (heater_on) {
    lh1500_on(13); /* Heater */
    printf("  >>> Heater ON! <<<\n");
  } else {
    lh1500_off(13); /* Heater */
    printf("  >>> Heater OFF! <<<\n");
  }
}

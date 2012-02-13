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

#include <bb/os.h>
#include <stdio.h>
#include <vegimeter.h>

unsigned iteration_counter = 0;

void ui_runner() {
  uint8_t i = 0;

  printf("----------------------- %d ----------------------\n", iteration_counter++);
  printf("Temperature for water sensor: %3.2fC\n", water_temperature);
  printf("Temperature for soil sensor A: %3.2fC\n", soil_temperature_a);
  printf("Temperature for soil sensor B: %3.2fC\n", soil_temperature_b);
  printf("Temperature for soil sensor C: %3.2fC\n", soil_temperature_c);
  printf("Temperature for soil sensor D: %3.2fC\n", soil_temperature_d);

  if(vegimeter_buttons) {
    for (i = 0; i < 8; i++, vegimeter_buttons >>= 1) {
      if (vegimeter_buttons & 1UL) {
	printf("Button pressed: %d\n", i);
      }
    }
  vegimeter_buttons = 0; /* was 'buttons' */
  }
}

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

#include <stdio.h>
#include <vegimeter.h>

#define SOIL_MIN_TEMP 2110  /* 21.1C. Almost 70F */
#define WATER_MAX_TEMP 5000 /* 50.0C. 104.0F */

void controller_runner(int water_temperature, int soil_temperature_a,
		       int soil_temperature_b, int soil_temperature_c,
		       int soil_temperature_d, int heater_on,
		       int pump_on) {
  /* Turn on the pump and heater if the soil is too cold */
  if((soil_temperature_a <= SOIL_MIN_TEMP) ||
     (soil_temperature_b <= SOIL_MIN_TEMP) ||
     (soil_temperature_c <= SOIL_MIN_TEMP) ||
     (soil_temperature_d <= SOIL_MIN_TEMP)) {
    heater_on = 1;
    pump_on = 1;
    printf("Pump and Heater ON\n");
  }

  /* Turn off the heater if the water is too warm */
  if(water_temperature > WATER_MAX_TEMP) {
    heater_on = 0;
    printf("Heater OFF\n");
  }

  /* Turn off the pump and heater if the soil is warm enough */
  if((soil_temperature_a > SOIL_MIN_TEMP) &&
     (soil_temperature_b > SOIL_MIN_TEMP) &&
     (soil_temperature_c > SOIL_MIN_TEMP) &&
     (soil_temperature_d > SOIL_MIN_TEMP)) {
    heater_on = 0;
    pump_on = 0;
    printf("Pump and Heater OFF\n");
  }
}

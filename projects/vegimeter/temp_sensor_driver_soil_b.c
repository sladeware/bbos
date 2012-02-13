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
#include <bb/os/drivers/onewire/onewire_bus.h>
#include <stdio.h>
#include <vegimeter.h>

void temp_sensor_driver_soil_b_runner(void) {
  /* This is P8X32A P10, QuickStart J1_11 & Vegimeter TS1 DQ */
  uint8_t pin = 10; /* QuickStart board */
  /* uint8_t pin = 2; */ /* DEMO Board */ 
  int err = 0;

  if (err = ds18b20_read_temperature(pin, &soil_temperature_b)) {
      printf("Temperature sensor on pin %d error: %d\n", pin, err);
  }
}

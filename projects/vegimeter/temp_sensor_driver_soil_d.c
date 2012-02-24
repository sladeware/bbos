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
#include <bb/os/drivers/onewire/slaves/ds18b20.h>
#include <stdio.h>
#include <vegimeter.h>

int
temp_sensor_driver_soil_d_runner()
{
  int soil_temperature_d;

  /* This is P8X32A 12, QuickStart J1_13 & Vegimeter TS1 DQ */
  uint8_t pin = 12; /* QuickStart board */
  /* uint8_t pin = 4; */ /* DEMO Board */
  int err = 0;

  if ((err = ds18b20_read_temperature(pin, &soil_temperature_d)))
    {
      printf("Temperature sensor on pin %d error: %d\n", pin, err);
    }

  return soil_temperature_d;
}

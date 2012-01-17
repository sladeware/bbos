/*

 * Copyright 2011 Sladeware LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *       http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#include <bb/os.h>
#include <bb/os/drivers/onewire/onewire_bus.h>
#include <bb/os/kernel/time.h>
#include <bb/builder/compilers/catalina/include/catalina_time.h>
#include <bb/builder/compilers/catalina/include/catalina_lmm.h>
#include <stdio.h>

void
temp_sensor_driver_soil_a_runner(void)
{
  /* This is P8X32A P8, QuickStart J1_9 & Vegimeter TS1 DQ */
  uint8_t pin = 0;
  int err = 0;
  static float temperature = 0.0;

  do {
    printf("Probing temperature for soil sensor A.\n");
    err = ds18b20_read_temperature(pin, &temperature);
    printf("  Result: %3.2f\n", temperature);
    delay_ms(3000);
  } while(1);
}

void
main()
{
  cog_id_t cog = 0;

  /* Start BBOS */
  bbos();

  /* TODO: Application threads on other cogs */

  /* Start the runner for this cog */
  temp_sensor_driver_soil_a_runner();
}

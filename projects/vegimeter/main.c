/* Copyright 2011 Sladeware LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include <bb/os.h>
#include <bb/os/kernel/delay.h>
#include <vegimeter.h>

/* This will eventually be replaced by real BBOS schedulers and running on multiple cogs */
int
main()
{
  unsigned delay = 10000; /* ms */

  printf("Starting Vegimeter!\n");
  
  do {
    controller_runner();

    button_driver_runner();
    heater_driver_runner();
    pump_driver_runner();
    temp_sensor_driver_water_runner();
    temp_sensor_driver_soil_a_runner();
    temp_sensor_driver_soil_b_runner();
    temp_sensor_driver_soil_c_runner();
    temp_sensor_driver_soil_d_runner();

    ui_runner();

    printf("Sleeping for %d ms\n", delay);
    bbos_delay_msec(delay);
  } while(1);

  return 0;
}

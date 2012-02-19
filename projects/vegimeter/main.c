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

/* This will eventually be replaced by real BBOS schedulers and running on multiple cogs */

#include <bb/os.h>
#include <bb/os/kernel/delay.h>
#include <vegimeter.h>

int
main()
{
  unsigned delay = 1000; /* ms */
  unsigned vegimeter_buttons = 0;
  int water_temperature = 0;
  int soil_temperature_a = 0;
  int soil_temperature_b = 0;
  int soil_temperature_c = 0;
  int soil_temperature_d = 0;
  unsigned heater_on = 0;
  unsigned pump_on = 0;

  printf("Starting Vegimeter!\n");
  
  do {
    controller_runner(water_temperature, soil_temperature_a, soil_temperature_b,
		      soil_temperature_c, soil_temperature_d,
		      soil_temperature_d, &heater_on, &pump_on);

    /* Button presses are hard detect until we're in a non-blocking context */
    vegimeter_buttons = button_driver_runner(vegimeter_buttons); 

    heater_driver_runner(heater_on);
    pump_driver_runner(pump_on);

    water_temperature = temp_sensor_driver_water_runner();
    soil_temperature_a = temp_sensor_driver_soil_a_runner();
    soil_temperature_b = temp_sensor_driver_soil_b_runner();
    soil_temperature_c = temp_sensor_driver_soil_c_runner();
    soil_temperature_d = temp_sensor_driver_soil_d_runner();

    ui_runner(water_temperature, soil_temperature_a, soil_temperature_b,
	      soil_temperature_c, soil_temperature_d,
	      soil_temperature_d, vegimeter_buttons);

    printf("Sleeping for %d ms\n", delay);
    bbos_delay_msec(delay);
  } while(1);

  return 0;
}

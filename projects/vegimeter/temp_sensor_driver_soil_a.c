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
#include <bb/os/kernel/time.h>
#include <bb/builder/compilers/catalina/include/catalina_time.h>
#include <bb/builder/compilers/catalina/include/catalina_lmm.h>


void
temp_sensor_driver_soil_a_runner(void)
{
  do {
    t_printf("Probing temperature for soil sensor A.\n");
    delay_ms(5000);
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


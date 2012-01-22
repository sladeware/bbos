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

/* define a default stack size to use for new cogs: */
#define STACK_SIZE 100

void
temp_sensor_driver_soil_a_runner(void)
{
  /* This is P8X32A P8, QuickStart J1_9 & Vegimeter TS1 DQ */
  uint8_t pin = 8; /* QuickStart board */
  /* uint8_t pin = 0; */ /* DEMO Board */ 

  int err = 0;
  static float temperature = 0.0;
  char whitespace[] = "   ";

  do {
    printf("Probing temperature for soil sensor A.\n");
    if (err = ds18b20_read_temperature(pin, &temperature))
      {
        printf("%sError: %d\n", whitespace, err);
      } else {
      printf("%sResult: %3.2fC\n", whitespace, temperature);
    }
    delay_ms(3000);
  } while(1);
}

void
main()
{
  /*  temp_sensor_driver_soil_a_runner(); */
  ui_runner();
}

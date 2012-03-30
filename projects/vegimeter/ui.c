/*
 * Copyright (c) 2012 Sladeware LLC
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
#include <bb/os/kernel/delay.h>
/* Processor dependent includes */
#include BBOS_PROCESSOR_FILE(shmem.h)
#include BBOS_PROCESSOR_FILE(sio.h)
#include BBOS_PROCESSOR_FILE(pins.h)

unsigned iteration_counter = 0;

#if 0
#include <vegimeter.h>
void
ui_runner(int water_temperature, int soil_temperature_a,
          int soil_temperature_b, int soil_temperature_c,
          int soil_temperature_d, unsigned vegimeter_buttons)
{
  uint8_t i = 0;

  printf("----------------------- %d ----------------------\n",
         iteration_counter++);
  printf("Temperature for water sensor: %i 1/100th degrees C\n",
         water_temperature);
  printf("Temperature for soil sensor A: %i 1/100th degrees C\n",
         soil_temperature_a);
  printf("Temperature for soil sensor B: %i 1/100th degrees C\n",
         soil_temperature_b);
  printf("Temperature for soil sensor C: %i 1/100th degrees C\n",
         soil_temperature_c);
  printf("Temperature for soil sensor D: %i 1/100th degrees C\n",
         soil_temperature_d);

  if (vegimeter_buttons)
    {
      for (i = 0; i < 8; i++, vegimeter_buttons >>= 1) {
        if (vegimeter_buttons & 1UL)
          {
            printf("Button pressed: %d\n", i);
          }
      }
      vegimeter_buttons = 0;
    }
}
#else

void
ui_runner()
{
  uint8_t i = 0;
  int8_t vegimeter_buttons;

#if 0
  bbos_printf("----------------------- %d ----------------------\n",
              iteration_counter++);
  bbos_printf("Temperature for water sensor: %i 1/100th degrees C\n",
              water_temperature);
  bbos_printf("Temperature for soil sensor A: %i 1/100th degrees C\n",
              soil_temperature_a);
  bbos_printf("Temperature for soil sensor B: %i 1/100th degrees C\n",
              soil_temperature_b);
  bbos_printf("Temperature for soil sensor C: %i 1/100th degrees C\n",
              soil_temperature_c);
  bbos_printf("Temperature for soil sensor D: %i 1/100th degrees C\n",
              soil_temperature_d);
#endif

  /* Read buttons state from the shared memory. */
  vegimeter_buttons = shmem_read_byte(VEGIMETER_BUTTONS_ADDR);

  if (vegimeter_buttons)
    {
      for (i = 0; i < 8; i++, vegimeter_buttons >>= 1)
        if (vegimeter_buttons & 1)
          bbos_printf("Button pressed: %d\n", i);
      /* Zero buttons state */
      shmem_write_byte(VEGIMETER_BUTTONS_ADDR, 0);
    }

}

void
bbos_kernel_loop()
{
  /* Do the main loop */
  while (TRUE)
    {
      ui_runner();
    }
}

int
main()
{
  /* Test ui running. Blink an LED that corresponds to the
     running COG id in order to define that our program is alive. */
#if 1
  propeller_set_dira_bits(1 << (16 + cogid()));
  propeller_set_outa_bits(1 << (16 + cogid()));
#endif

  sio_init();

  bbos_kernel_loop();

  return 0;
}
#endif

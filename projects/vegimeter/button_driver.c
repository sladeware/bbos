/*
 * Copyright 2012 Sladeware LLC
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
#include <bb/os/drivers/gpio/button.h>
#include BBOS_PROCESSOR_FILE(shmem.h)
#include BBOS_PROCESSOR_FILE(sio.h)
#include BBOS_PROCESSOR_FILE(pins.h)
/* Application configs */
#include "button_driver.h"

void
bbos_kernel_loop()
{
  /* Do the main loop */
  while (TRUE)
    {
      button_driver_runner();
    }
}

void
button_driver_runner()
{
  uint16_t vegimeter_buttons;
  /* QuickStart board has P0 - P7 as buttons */
  int16_t button_mask = 0xFFUL;

  /* Read, update and store pressed buttons on vegimeter device.
     We need just one byte from the button mask. */
  vegimeter_buttons = shmem_read_byte(VEGIMETER_BUTTONS_ADDR);
  vegimeter_buttons = (int8_t)are_buttons_pressed(button_mask); /* |=?*/
  shmem_write_byte(VEGIMETER_BUTTONS_ADDR, vegimeter_buttons);
}

int
main()
{
  /* Test button driver running. Blink an LED that corresponds to the
     running COG id in order to define, that our program is alive. */
#if 0
  propeller_set_dira_bits(1 << (16 + cogid()));
  propeller_set_outa_bits(1 << (16 + cogid()));
#endif

  /* Initialize shared memory area. */
  shmem_write_byte(VEGIMETER_BUTTONS_ADDR, 0);

  /* Initialize SIO driver for communication purposes */
  sio_init();

  /* Start Bionic Bunny OS */
  bbos_kernel_loop();

  return 0;
}


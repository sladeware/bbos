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

#include "button_driver.h"
//#include "vegimeter.h"

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
  uint16_t button_mask = 0xFFUL; /* QuickStart board has P0 - P7 as buttons */

  bbos_delay_msec(3000);

  shmem_read(VEGIMETER_BUTTONS_ADDR, &vegimeter_buttons, 2);
  vegimeter_buttons |= are_buttons_pressed(button_mask);
  shmem_write(VEGIMETER_BUTTONS_ADDR, &vegimeter_buttons, 2);
  sio_printf((const int8_t*)"Buttons: %d\n", vegimeter_buttons);
}

int
main()
{
  /* Test button driver running. Blink an LED that corresponds to the
     running COG id in order to define that our program is alive. */
  //DIR_OUTPUT((1 << 4) + cogid());
  //OUT_HIGH((1 << 4) + cogid());

  /* Start Bionic Bunny OS */
  bbos();
  return 0;
}

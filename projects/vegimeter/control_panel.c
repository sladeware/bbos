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

/* Application configs */
#include "vegimeter_config.h"

#include <bb/os.h>
#include <bb/os/kernel/delay.h>
#include <bb/os/drivers/gpio/button.h>
#include BBOS_PROCESSOR_FILE(shmem.h)
#include BBOS_PROCESSOR_FILE(sio.h)
#include BBOS_PROCESSOR_FILE(pins.h)

static int8_t buttons_state = 0;

void
control_panel_runner()
{
  int8_t i;
  uint16_t vegimeter_buttons;
  /* QuickStart board has P0 - P7 as buttons */
  int16_t button_mask = 0xFFUL;

  /* Read, update and store pressed buttons on vegimeter device.
     We need just one byte from the button mask. */
  vegimeter_buttons = shmem_read_byte(VEGIMETER_BUTTONS_ADDR);
  vegimeter_buttons = (int8_t)are_buttons_pressed(button_mask); /* |=?*/
  shmem_write_byte(VEGIMETER_BUTTONS_ADDR, vegimeter_buttons);
  for (i = 0; i < 8; i++) {
    if (vegimeter_buttons & GET_MASK(i)) {
      buttons_state ^= GET_MASK(i);
      DIR_TO(16 + i, !!(buttons_state & GET_MASK(i)));
      OUT_TO(16 + i, !!(buttons_state & GET_MASK(i)));
    }
  }
}

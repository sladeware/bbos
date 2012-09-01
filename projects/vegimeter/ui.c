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

#include "vegimeter_config.h"

#include <bb/os.h>
#include <bb/os/kernel/delay.h>
#include BBOS_PROCESSOR_FILE(shmem.h)
#include BBOS_PROCESSOR_FILE(sio.h)

void
ui_runner()
{
  uint8_t i = 0;
  int8_t vegimeter_buttons;
  /* Read buttons state from the shared memory. */
  vegimeter_buttons = shmem_read_byte(VEGIMETER_BUTTONS_ADDR);
  if (vegimeter_buttons) {
    for (i = 0; i < 8; i++, vegimeter_buttons >>= 1) {
      if (vegimeter_buttons & 1) {
        sio_printf((int8_t*)"Button pressed: %d\n", i);
      }
    }
    /* Zero buttons state */
    shmem_write_byte(VEGIMETER_BUTTONS_ADDR, 0);
  }
}

/*
 * One wire device I/O support.
 *
 * Copyright (c) 2012 Sladeware LLC
 * Author: Oleksandr Sviridenko
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

#ifndef __BB_OS_DRIVERS_ONEWIRE_BUS_H
#define __BB_OS_DRIVERS_ONEWIRE_BUS_H

#include <bb/os.h>
#include <bb/os/kernel/delay.h>
#include BBOS_PROCESSOR_FILE(pins.h)

/* ROM commands */
enum {
  /* Read the 64-bit ID of the 1-Wire device;serial num; CRC */
  OW_READ_ROM = 0x33,
  /* Look for specific device */
  OW_MATCH_ROM = 0x55,
  /* Skip rom (one device)  */
  OW_SKIP_ROM = 0xCC,
  /* Search */
  OW_SEARCH_ROM = 0xF0,
  OW_ALARM_SEARCH_ROM = 0xEC,
};

/* Remember that pins start at 0 */
#define OW_GET_INPUT(pin)  GET_INPUT(pin)
#define OW_DIR_OUTPUT(pin) DIR_OUTPUT(pin)
#define OW_DIR_INPUT(pin)  DIR_INPUT(pin)
#define OW_OUT_LOW(pin)    OUT_LOW(pin)
#define OW_OUT_HIGH(pin)   OUT_HIGH(pin)

/* Sleep macro */
#define ow_delay_usec(usecs) bbos_delay_usec(usecs)

/* Prototypes */

uint8_t ow_reset(uint8_t pin);
#define ow_read_byte(pin) ow_io_byte(0xFF, pin)
#define ow_write_byte(byte, pin) ow_io_byte(byte, pin)
uint8_t ow_io_byte(uint8_t byte, uint8_t pin);
uint8_t ow_io_bit(uint8_t bit, uint8_t pin);
unsigned ow_input_pin_state(uint8_t pin);
void ow_command(uint8_t cmd, uint8_t pin);

#endif /* __BB_OS_DRIVERS_ONEWIRE_BUS_H */

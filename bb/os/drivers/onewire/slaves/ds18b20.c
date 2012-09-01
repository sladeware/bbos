/*
 * This file implements DS18B20 temp sensor interface.
 *
 * Copyright (c) 2012 Sladeware LLC
 * Author: Oleksandr Sviridenko
 */

#include "ds18b20.h"

#include <bb/os.h>
#include <bb/os/drivers/onewire/onewire_bus.h>

int
ds18b20_read_temperature(uint8_t pin, int* value)
{
  uint8_t i;
  uint8_t sp[DS18B20_SCRATCHPAD_SIZE];
  int sign;
  int temp_data;

  *value = DEFAULT_TEMP_READING;
  ow_reset(pin);
  /* Start measurements... */
  if (ow_reset(pin)) {
    printf("Failed to reset 1-wire BUS before reading sensor's ROM.\r\n");
    return 3;
  }
  /*
   * Now we need to read the state from the input pin to define
   * whether the bus is "idle".
   */
  if (!ow_input_pin_state(pin)) {
    return 2;
  }
  ow_command(DS18B20_CONVERT_TEMPERATURE, pin);
  if (ow_reset(pin)) {
    printf("Failed to reset 1-wire BUS before reading sensor's ROM.\r\n");
    return 1;
  }
  ow_command(DS18B20_READ_SCRATCHPAD, pin);
  for (i=0; i<DS18B20_SCRATCHPAD_SIZE; i++) {
    sp[i] = ow_read_byte(pin);
  }
  /* Process measurements... */
  sign = sp[1] & 0xF0 ? -1 : 1; /* sign */
  temp_data = ((unsigned)(sp[1] & 0x07) << 8) | sp[0];
  *value = DS18B20_1_100TH_CELCIUS((temp_data & 0xFFFF) * sign) >> 4;
  return 0;
}

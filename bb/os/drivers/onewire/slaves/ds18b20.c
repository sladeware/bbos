/*
 * This file implements DS18B20 temp sensor interface.
 *
 * Copyright (c) 2012 Sladeware LLC
 * Author: Oleksandr Sviridenko
 */

#include "ds18b20.h"

#include <bb/os/drivers/onewire/onewire_bus.h>

/* Read scratch pad. */
#define DS18B20_READ_SCRATCHPAD 0xBE
/* Write scratch pad. */
#define DS18B20_WRITE_SCRATCHPAD 0x4E
/* Start temperature conversion. */
#define DS18B20_CONVERT_TEMPERATURE 0x44
/* Read power status. */
#define DS18B20_READ_POWER 0xB4
/* Scratch pad size in bytes. */
#define DS18B20_SCRATCHPAD_SIZE 9

#define DEFAULT_TEMP_READING 54321

/*
 * Reads temperature (scratchpad) from sensor.
 *
 * The value DEFAULT_TEMP_READING is set upon error and > 0 is returned. Returns 0
 * on success.
 */
void
ds18b20_read_temperature(void* input, void* output)
{
  int16_t pin;
  int* value;
  int8_t* err;
  uint8_t i;
  uint8_t sp[DS18B20_SCRATCHPAD_SIZE];
  int sign;
  int temp_data;

  pin = ((struct ds18b20_input* )input)->pin;
  value = ((struct ds18b20_output* )output)->value;
  err = ((struct ds18b20_output*)output)->err;
  *err = 0;

  *value = DEFAULT_TEMP_READING;
  ow_reset(pin);
  /* Start measurements... */
  if (ow_reset(pin)) {
    printf("Failed to reset 1-wire BUS before reading sensor's ROM.\r\n");
    *err = 3;
    return;
  }
  /*
   * Now we need to read the state from the input pin to define
   * whether the bus is "idle".
   */
  if (!ow_input_pin_state(pin)) {
    *err = 2;
    return;
  }
  ow_command(DS18B20_CONVERT_TEMPERATURE, pin);
  if (ow_reset(pin)) {
    printf("Failed to reset 1-wire BUS before reading sensor's ROM.\r\n");
    *err = 1;
    return;
  }
  ow_command(DS18B20_READ_SCRATCHPAD, pin);
  for (i=0; i<DS18B20_SCRATCHPAD_SIZE; i++) {
    sp[i] = ow_read_byte(pin);
  }
  /* Process measurements... */
  sign = sp[1] & 0xF0 ? -1 : 1; /* sign */
  temp_data = ((unsigned)(sp[1] & 0x07) << 8) | sp[0];
  *value = DS18B20_1_100TH_CELCIUS((temp_data & 0xFFFF) * sign) >> 4;
}

#include "ds18b20_driver_runner_autogen.c"

/*
 * Copyright (c) 2012 Sladeware LLC
 */

/**
 * @file bb/os/drivers/onewire/slaves/ds18b20.c
 * @brief DS18B20 temp sensor
 */

#include <bb/os.h>
#include <bb/os/drivers/onewire/slaves/ds18b20.h>
#include <bb/os/drivers/onewire/onewire_bus.h>

/**
 * Read temperature (scratchpad) of sensor.
 *
 * The pin argument is the P8X32A GPIO pin that connects to the DS18B20's DQ
 * It starts at 0 and goes to 31.
 */
int
ds18b20_read_temperature(uint8_t pin, float* value)
{
  uint8_t i;
  uint8_t sp[DS18B20_SCRATCHPAD_SIZE];
  int sign;
  int temp_data;

  ow_reset(pin);

  /* Start measurements */
  if (ow_reset(pin))
    {
      printf("Failed to reset 1-wire BUS before reading sensor's ROM.\r\n");
      return 1;
    }

  /*
   * Now we need to read the state from the input pin to define
   * whether the bus is "idle".
   */

  if (!ow_input_pin_state(pin))
    {
      return 1;
    }

  ow_command(DS18B20_CONVERT_TEMPERATURE, pin);

  if (ow_reset(pin))
    {
      printf("Failed to reset 1-wire BUS before reading sensor's ROM.\r\n");
      return 1;
    }

  ow_command(DS18B20_READ_SCRATCHPAD, pin);

  for (i=0; i<DS18B20_SCRATCHPAD_SIZE; i++)
    {
      sp[i] = ow_read_byte(pin);
    }

  /* Process measurements */
  sign = sp[1] & 0xF0 ? -1 : 1; /* sign */
  temp_data = ((unsigned int)(sp[1] & 0x07) << 8) | sp[0];
	*value = ((float)((temp_data & 0xFFFF) * sign)) / 16.0;

  return 0;
}

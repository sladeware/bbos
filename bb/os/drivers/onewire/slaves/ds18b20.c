/*
 * Copyright (c) 2012 Sladeware LLC
 */

/**
 * @file bb/os/drivers/onewire/slaves/ds18b20.c
 * @brief DS18B20 temp sensor
 */

#include <bbos.h>
#include <bb/os/drivers/onewire/slaves/ds18b20.h>
#include <bb/os/drivers/onewire/bus.h>

/**
 * Read temperature (scratchpad) of sensor.
 */
float
ds18b20_read_temperature()
{
  uint8_t i;
  uint8_t sp[DS18B20_SCRATCHPAD_SIZE];
  int sign;
  int temp_data;
  
  /* Start measurements */
  if (!ow_reset())
    {
      printf("Failed to reset 1-wire BUS before reading sensor's ROM.\r\n");
      return 1;
    }
  /*
   * Now we need to read the state from the input pin to define
   * whether the bus is "idle".
   */
  if (!ow_input_pin_state())
    {
      return 1;
    }
  ow_command(DS18B20_CONVERT_TEMPERATURE);
  
  if (!ow_reset())
    {
      printf("Failed to reset 1-wire BUS before reading sensor's ROM.\r\n");
      return 1;
    }
  ow_command(DS18B20_READ_SCRATCHPAD);
  for (i=0; i<DS18B20_SCRATCHPAD_SIZE; i++)
    {
      sp[i] = ow_read_byte();
    }

  /* Process measurements */

  sign = sp[1] & 0xF0 ? -1 : 1; /* sign */
  temp_data = ((int)(sp[1] & 0x07) << 8) | sp[0];
  
  return ((float)(temp_data * sign)) / 16.0;
}


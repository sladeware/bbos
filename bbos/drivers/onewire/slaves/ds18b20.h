/*
 * DS18B20 temp sensor.
 *
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */
 
#ifndef __DS18B20_H
#define __DS18B20_H

#include <bbos/kernel.h>

#define DS18B20_READ_SCRATCHPAD	0xBE // read scratch pad
#define DS18B20_WRITE_SCRATCHPAD 0x4E
#define DS18B20_CONVERT_TEMPERATURE	0x44 // start temperature conversion
#define DS18B20_READ_POWER 0xB4

#define DS18B20_SCRATCHPAD_SIZE 9 // bytes

/* Prototypes */

uint8_t ds18b20_request_data();
uint8_t ds18b20_read_data();

#endif 


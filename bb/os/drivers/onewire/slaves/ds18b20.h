/*
 * DS18B20 temp sensor interface.
 *
 * Copyright (c) 2012 Sladeware LLC
 * Author: Oleksandr Sviridenko
 */

#ifndef __BB_OS_DRIVERS_ONEWIRE_SLAVES_DS18B20_H
#define __BB_OS_DRIVERS_ONEWIRE_SLAVES_DS18B20_H

#include <bb/os/config.h>

/* Read scratch pad. */
#define DS18B20_READ_SCRATCHPAD      0xBE
/* Write scratch pad. */
#define DS18B20_WRITE_SCRATCHPAD     0x4E
/* Start temperature conversion. */
#define DS18B20_CONVERT_TEMPERATURE  0x44
/* Read power status. */
#define DS18B20_READ_POWER           0xB4
/* Scratch pad size in bytes. */
#define DS18B20_SCRATCHPAD_SIZE      9

#define DEFAULT_TEMP_READING 54321

/* Useful macros */

#define DS18B20_1_100TH_CELCIUS(value) (100 * (value))

/* Prototypes */

/*
 * Reads temperature (scratchpad) from sensor.
 *
 * The pin argument is the P8X32A GPIO pin that connects to the DS18B20's DQ
 * It starts at 0 and goes to 31.
 *
 * The *value argument contains the resulting temperature reading. It is an
 * integer that represents 1/100ths of degrees Celcius. For example:
 *   23.51C at the sensor => *value = 2351.
 *
 * The *value -54321 is set upon error and > 0 is returned. Returns 0 on success
 */
int ds18b20_read_temperature(uint8_t pin, int* value);

#endif /* __BB_OS_DRIVERS_ONEWIRE_SLAVES_DS18B20_H */

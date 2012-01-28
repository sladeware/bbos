/*
 * Copyright (c) 2012 Sladeware LLC
 */

/**
 * @file bb/os/drivers/onewire/slaves/ds18b20.h
 * @brief DS18B20 temp sensor interface
 */

#ifndef __DS18B20_H
#define __DS18B20_H

#include <bb/os/config.h>

/** Read scratch pad. */
#define DS18B20_READ_SCRATCHPAD      0xBE
/** Write scratch pad. */
#define DS18B20_WRITE_SCRATCHPAD     0x4E
/** Start temperature conversion. */
#define DS18B20_CONVERT_TEMPERATURE  0x44
/** Read power status. */
#define DS18B20_READ_POWER           0xB4
/** Scratch pad size in bytes. */
#define DS18B20_SCRATCHPAD_SIZE      9

/* Prototypes */
int ds18b20_read_temperature(uint8_t pin, float* value);

#endif /* __DS18B20_H */
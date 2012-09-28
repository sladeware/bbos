/*
 * DS18B20 temp sensor interface.
 *
 * Copyright (c) 2012 Sladeware LLC
 * Author: Oleksandr Sviridenko
 */
#ifndef __BB_OS_DRIVERS_ONEWIRE_SLAVES_DS18B20_H
#define __BB_OS_DRIVERS_ONEWIRE_SLAVES_DS18B20_H

#include <bb/os/config.h>
#include "ds18b20_driver_runner_autogen.h"

#define DS18B20_1_100TH_CELCIUS(value) (100 * (value))

/**
 * The pin field is the P8X32A GPIO pin that connects to the
 * DS18B20's DQ. It starts at 0 and goes to 31.
 */
struct ds18b20_input {
  int16_t* pin;
};

/**
 * The value field contains the resulting temperature reading. It
 * is an integer that represents 1/100ths of degrees Celcius. For
 * example: 23.51C at the sensor => *value = 2351.
 */
struct ds18b20_output {
  int16_t* value;
  int8_t* err;
};

#endif /* __BB_OS_DRIVERS_ONEWIRE_SLAVES_DS18B20_H */

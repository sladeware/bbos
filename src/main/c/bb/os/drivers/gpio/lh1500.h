/*
 * Copyright (c) 2012-2013 Sladeware LLC
 * http://www.bionicbunny.org/
 */

/**
 * @file bb/os/drivers/gpio/lh1500.h
 * @brief LH1500 Solid State Relay Support
 */

#ifndef __BB_OS_DRIVERS_GPIO_LH1500_H
#define __BB_OS_DRIVERS_GPIO_LH1500_H

#include "bb/os.h"
#include BBOS_PROCESSOR_FILE(pins.h)

void lh1500_on(uint8_t pin);
void lh1500_off(uint8_t pin);

#endif /* __BB_OS_DRIVERS_GPIO_LH1500_H */

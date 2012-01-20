/*
 * Copyright (c) 2012 Sladeware LLC
 */

/**
 * @file bb/os/drivers/gpio/lh1500.h
 * @brief LH1500 Solid State Relay Support
 */

#ifndef __LH1500_H
#define __LH1500_H

#include <bb/os/drivers/processors/propeller_p8x32/pins.h>

void lh1500_on(uint8_t pin);
void lh1500_off(uint8_t pin);

#endif /* __LH1500_h */

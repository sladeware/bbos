/*
 * Copyright (c) 2012 Sladeware LLC
 */

/**
 * @file bb/os/drivers/processors/propeller_p8x32/pins.h
 * @brief Parallax Propeller P8X32A GPIO Pin Support
 */

#ifndef __PINS_H
#define __PINS_H

/* Pins start at 0. There are 32 Pins. P0 - P31 */
#define GET_DPIN(pin)   (1UL << pin)
#define GET_INPUT(pin)  (_ina() & GET_DPIN(pin))
#define DIR_OUTPUT(pin) (_dira(GET_DPIN(pin), GET_DPIN(pin)))
#define DIR_INPUT(pin)  (_dira(GET_DPIN(pin), 0))
#define OUT_LOW(pin)    (_outa(GET_DPIN(pin), 0))
#define OUT_HIGH(pin)   (_outa(GET_DPIN(pin), GET_DPIN(pin)))

#endif /* __PINS_H */

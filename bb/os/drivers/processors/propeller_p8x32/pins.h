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
#define GET_MASK(pin)   (1UL << pin)

#define GET_INPUT(pin)  (_ina() & GET_MASK(pin))
#define DIR_OUTPUT(pin) (_dira(GET_MASK(pin), GET_MASK(pin)))
#define DIR_INPUT(pin)  (_dira(GET_MASK(pin), 0))
#define OUT_LOW(pin)    (_outa(GET_MASK(pin), 0))
#define OUT_HIGH(pin)   (_outa(GET_MASK(pin), GET_MASK(pin)))

#define GET_INPUT_MASK(mask)  (_ina() & (unsigned)mask)
#define DIR_OUTPUT_MASK(mask) (_dira((unsigned)mask, (unsigned)mask))
#define DIR_INPUT_MASK(mask)  (_dira((unsigned)mask, 0))
#define OUT_LOW_MASK(mask)    (_outa((unsigned)mask, 0))
#define OUT_HIGH_MASK(mask)   (_outa((unsigned)mask, (unsigned)mask))

#endif /* __PINS_H */

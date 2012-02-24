/*
 * Copyright (c) 2012 Sladeware LLC
 */

/**
 * @file bb/os/drivers/processors/propeller_p8x32/pins.h
 * @brief Parallax Propeller P8X32A GPIO Pin Support
 */

#ifndef __PINS_H
#define __PINS_H

#include <bb/os/config.h>

#ifdef __CATALINA__
/* Set pins in DIRA */
#define bbos_pins_set_dira(bits) _dira((bits), (bits))
#define bbos_pins_clr_dira(bits) _dira((bits), 0)
#define bbos_pins_set_outa(bits) _outa((bits), (bits))
#define bbos_pins_clr_outa(bits) _outa((bits), 0)
#define bbos_pins_get_ina() _ina()
#elif __GNUC__
//#include <propeller.h>
#define bbos_pins_set_dira(bits) DIRA |= (bits)
#define bbos_pins_clr_dira(bits) DIRA &= ~(bits)
#define bbos_pins_set_outa(bits) OUTA |= (bits)
#define bbos_pins_clr_outa(bits) OUTA &= ~(bits)
#define bbos_pins_get_ina() INA
#else
#error This compiler is not supported. Please report support team.
#endif

/* Pins start at 0. There are 32 Pins. P0 - P31 */
#define GET_MASK(pin)   (1UL << pin)

#define GET_INPUT(pin)  (bbos_pins_get_ina() & GET_MASK(pin))
#define DIR_OUTPUT(pin) (bbos_pins_set_dira(GET_MASK(pin)))
#define DIR_INPUT(pin)  (bbos_pins_clr_dira(GET_MASK(pin)))
#define OUT_LOW(pin)    (bbos_pins_clr_outa(GET_MASK(pin)))
#define OUT_HIGH(pin)   (bbos_pins_set_outa(GET_MASK(pin)))

#define GET_INPUT_MASK(mask)  (bbos_pins_get_ina() & (unsigned)mask)
#define DIR_OUTPUT_MASK(mask) (bbos_pins_set_dira((unsigned)mask))
#define DIR_INPUT_MASK(mask)  (bbos_pins_clr_dira((unsigned)mask))
#define OUT_LOW_MASK(mask)    (bbos_pins_clr_outa((unsigned)mask))
#define OUT_HIGH_MASK(mask)   (bbos_pins_set_outa((unsigned)mask))

#endif /* __PINS_H */

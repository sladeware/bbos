/*
 * Copyright (c) 2012 Sladeware LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/**
 * @file bb/os/drivers/processors/propeller_p8x32/pins.h
 * @brief Parallax Propeller P8X32A GPIO Pin Support
 * @note This implementatin has to be independent from BBOS.
 */

#ifndef __PROPELLER_P8X32_PINS_H
#define __PROPELLER_P8X32_PINS_H

#include <bb/types.h>
#include <bb/os/drivers/processors/propeller_p8x32/config.h>

#ifdef __CATALINA__
/* Update bits of DIRA register */
#  defein propeller_set_dira_bit(bits, v) _dira((bits), (v))
#  define propeller_set_dira_bits(bits) _dira((bits), (bits))
#  define propeller_clr_dira_bits(bits) _dira((bits), 0)
/* Update bits of OUTA register */
#  define propeller_set_outa_bit(bits, v) _outa((bits), (v))
#  define propeller_set_outa_bits(bits) _outa((bits), (bits))
#  define propeller_clr_outa_bits(bits) _outa((bits), 0)
#  define proepller_get_ina_bits() _ina()

#if 0 /* XXX: obsolete API, will be removed ASAP */
#  define bbos_pins_set_dira(bits, v) _dira((bits), (v))
#  define bbos_pins_fix_dira(bits) _dira((bits), (bits))
#  define bbos_pins_clr_dira(bits) _dira((bits), 0)
#  define bbos_pins_set_outa(bits, v) _outa((bits), (v))
#  define bbos_pins_fix_outa(bits) _outa((bits), (bits))
#  define bbos_pins_clr_outa(bits) _outa((bits), 0)
#  define bbos_pins_get_ina() _ina()
#endif

#elif __GNUC__

/* Update bits of DIRA register */
#  define propeller_set_dira_bit(bits, v) DIRA = (DIRA &~ (bits)) | (v)
#  define propeller_set_dira_bits(bits) DIRA |= (bits)
#  define propeller_clr_dira_bits(bits) DIRA &= ~(bits)
/* Update bits of OUTA register */
#  define propeller_set_outa_bit(bits, v) OUTA = (OUTA &~ (bits)) | (v)
#  define propeller_set_outa_bits(bits) OUTA |= (bits)
#  define propeller_clr_outa_bits(bits) OUTA &= ~(bits)
#  define propeller_get_ina_bits() INA

#if 0 /* XXX: obsolete API */
#  define bbos_pins_set_dira(bits, state) DIRA = (DIRA &~ (bits)) | (state)
#  define bbos_pins_fix_dira(bits) DIRA |= (bits)
#  define bbos_pins_clr_dira(bits) DIRA &= ~(bits)
#  define bbos_pins_set_outa(bits, state) OUTA = (OUTA &~ (bits)) | (state)
#  define bbos_pins_fix_outa(bits) OUTA |= (bits)
#  define bbos_pins_clr_outa(bits) OUTA &= ~(bits)
#  define bbos_pins_get_ina() INA
#endif

#else
#  error This compiler is not supported. Please report support team.
#endif

/* Pins start at 0. There are 32 Pins. P0 - P31 */
#define GET_MASK(pin) (1UL << (pin))

#define GET_INPUT(pin) ((propeller_get_ina_bits() >> (pin)) & 1)
#define DIR_OUTPUT(pin) (propeller_set_dira_bits(GET_MASK(pin)))
#define DIR_INPUT(pin) (propeller_clr_dira_bits(GET_MASK(pin)))
#define DIR_TO(pin, state) (propeller_set_dira_bit(GET_MASK(pin), (state) << (pin)))
#define OUT_LOW(pin) (propeller_clr_outa_bits(GET_MASK(pin)))
#define OUT_HIGH(pin) (propeller_set_outa_bits(GET_MASK(pin)))
#define OUT_TO(pin, state) (propeller_set_outa_bit(GET_MASK(pin), (state) << (pin)))

#define GET_INPUT_MASK(mask) (propeller_get_ina_bits() & (unsigned)mask)
#define DIR_OUTPUT_MASK(mask) (propeller_set_dira_bits((unsigned)mask))
#define DIR_INPUT_MASK(mask) (propeller_clr_dira_bits((unsigned)mask))
#define OUT_LOW_MASK(mask) (propeller_clr_outa_bits((unsigned)mask))
#define OUT_HIGH_MASK(mask) (propeller_set_outa_bits((unsigned)mask))

#endif /* __PROPELLER_P8X32_PINS_H */

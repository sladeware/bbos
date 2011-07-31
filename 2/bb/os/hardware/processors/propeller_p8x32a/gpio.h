/*
 * Copyright (c) 2011 Sladeware LLC
 */

#ifndef __GPIO_H
#define __GPIO_H

#ifndef __CATALINA__
#error ""Unsupported compiler
#endif

#include <catalina_cog.h>

/* To configure direction as input */
#define GPIOA_DIRECTION_INPUT 0
/* To configure direction as output */
#define GPIOA_DIRECTION_OUTPUT 1
/* As output, set initial level to low */
#define GPIOA_INIT_LOW 0
/* As output, set initial level to high */
#define GPIOA_INIT_HIGH 1

#define GET_PIN(pin) (1<<(pin))

#define GPIOA_SET_DIRECTION(pin, direction) _dira(GET_PIN(pin), direction)
#define GPIOA_SET_VALUE(pin, value) _outa(GET_PIN(pin), value)
#define GPIOA_GET_VALUE(pin) (!!(_ina() & GET_PIN(pin)))

#define GPIOA_SET_HIGH(pin) _outa(GET_PIN(pin), GET_PIN(pin))
#define GPIOA_SET_LOW(pin) _outa(GET_PIN(pin), 0)
#define GPIOA_SET_INPUT(pin) _dira(GET_PIN(pin), 0)
#define GPIOA_SET_OUTPUT(pin) _dira(GET_PIN(pin), GET_PIN(pin))

#define GPIOA_SET_GROUP_OUTPUT(first, last) _dira(GET_PIN((last)+1) - GET_PIN(first), GET_PIN((last)+1) - GET_PIN(first))

#endif


/*
 * Copyright (c) 2011 Sladeware LLC
 */

#ifndef __PROCESSOR_GPIO_H
#define __PROCESSOR_GPIO_H

#ifndef __CATALINA__
#error "Unsupported compiler: this implementation only supports " \
  "Catalina compiler"
#endif

/**
 * P8X32A supports GPIO Port A with 32 pins: P0 - P31.
 */
#define PROCESSOR_NUM_GPIOS 32

#include <catalina_cog.h>

/**
 * Valid GPIOs are nonnegative.
 */
#define GPIO_IS_VALID(gpio) ((unsigned gpio) < PROCESSOR_NUM_GPIOS)

/* To configure direction as input */
#define GPIO_DIRECTION_INPUT 0
/* To configure direction as output */
#define GPIO_DIRECTION_OUTPUT 1
/* As output, set initial level to low */
#define GPIO_INIT_LOW 0
/* As output, set initial level to high */
#define GPIO_INIT_HIGH 1

#define GET_PIN(pin) (1<<(pin))

#define GPIO_SET_DIRECTION(pin, direction) _dira(GET_PIN(pin), direction)
#define GPIO_SET_VALUE(pin, value) _outa(GET_PIN(pin), value)
#define GPIO_GET_VALUE(pin) (!!(_ina() & GET_PIN(pin)))

#define GPIO_SET_HIGH(pin) _outa(GET_PIN(pin), GET_PIN(pin))
#define GPIO_SET_LOW(pin) _outa(GET_PIN(pin), 0)
#define GPIO_SET_INPUT(pin) _dira(GET_PIN(pin), 0)
#define GPIO_SET_OUTPUT(pin) _dira(GET_PIN(pin), GET_PIN(pin))

#define GPIO_SET_GROUP_OUTPUT(first, last) \
  _dira(GET_PIN((last)+1) - GET_PIN(first), GET_PIN((last)+1) - GET_PIN(first))

#endif /* __PROCESSOR_GPIO_H */

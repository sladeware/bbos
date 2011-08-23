/*
 * Copyright (c) 2011 Sladeware LLC
 */

#ifndef __PROCESSOR_GPIO_H
#define __PROCESSOR_GPIO_H

/**
 * @file gpio.h
 * @brief Propeller P8X32 GPIO support
 */

#ifndef __CATALINA__
#error "Unsupported compiler: this implementation only supports " \
  "Catalina compiler"
#endif

/**
 * @def PROCESSOR_NUM_GPIOS
 * @brief P8X32A supports GPIO Port A with 32 pins: P0 - P31.
 */
#define PROCESSOR_NUM_GPIOS 32

#include <catalina_cog.h>

/**
 * @def GPIO_IS_VALID(gpio)
 * @brief Valid GPIOs are nonnegative.
 */
#define GPIO_IS_VALID(gpio) ((unsigned gpio) < PROCESSOR_NUM_GPIOS)

#define GET_PIN(pin) (1<<(pin))

#define GPIO_SET_DIRECTION(pin, direction) _dira(GET_PIN(pin), direction)
#define GPIO_SET_VALUE(pin, value) _outa(GET_PIN(pin), value)
#define GPIO_GET_VALUE(pin) (!!(_ina() & GET_PIN(pin)))

#define GPIO_SET_HIGH(pin) _outa(GET_PIN(pin), GET_PIN(pin))
#define GPIO_SET_LOW(pin) _outa(GET_PIN(pin), 0)
#define GPIO_DIRECTION_INPUT(pin) _dira(GET_PIN(pin), 0)
#define GPIO_DIRECTION_OUTPUT(pin) _dira(GET_PIN(pin), GET_PIN(pin))

#define GPIO_SET_GROUP_OUTPUT(first, last) \
  _dira(GET_PIN((last)+1) - GET_PIN(first), GET_PIN((last)+1) - GET_PIN(first))

#endif /* __PROCESSOR_GPIO_H */

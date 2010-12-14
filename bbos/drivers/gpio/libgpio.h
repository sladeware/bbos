/*
 * GPIO programming interface.
 *
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

#ifndef __LIBGPIO_H
#define __LIBGPIO_H

#include <bbos/kernel.h>

/*
 * GPIO_NUMBER_OF_PINS defines valid GPIO numbers to be in the range 0..MAX_INT,
 * this library restricts them to the smaller range 0..GPIO_NUMBER_OF_PINS-1.
 */
#ifndef GPIO_NUMBER_OF_PINS
#define GPIO_NUMBER_OF_PINS 256
#endif

struct gpio_chip {
  int8_t *label; // label
  int16_t base; // the very first pin number
  uint16_t n; // the number of pins handled by this chip
};

struct gpio_pin {
  struct gpio_chip *chip; // chip to which this pin belongs
  int16_t owner; // identifier which owns this pin
};

extern struct gpio_pin gpio_table[GPIO_NUMBER_OF_PINS];

#define gpio_pin_to_chip(pin) gpio_table[pin].chip

#pragma BBOS messages(GPIO_OPEN=BBOS_DRIVER_OPEN, GPIO_CLOSE=BBOS_DRIVER_CLOSE,\
	GPIO_DIRECTION_INPUT, GPIO_DIRECTION_OUTPUT, GPIO_SET_VALUE, GPIO_GET_VALUE)


struct gpio_message {
	uint16_t owner;
  uint32_t pin;
  uint32_t value;
  bbos_return_t error;
};

int16_t gpio_register_chip(struct gpio_chip *chip);

int16_t gpio_unregister_chip(struct gpio_chip *chip);

#endif /* __BBOS_GPIO_DRIVER_H */


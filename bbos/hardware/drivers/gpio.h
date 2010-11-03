/*
 * GPIO programming interface.
 *
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_GPIO_DRIVER_H
#define __BBOS_GPIO_DRIVER_H

#include <bbos/hardware/driver.h>

/*
 * BBOS_GPIO_NUMBER_OF_PINS defines valid GPIO numbers to be in the range 
 * 0..MAX_INT, this library restricts them to the smaller range 
 * 0..BBOS_GPIO_NUMBER_OF_PINS-1.
 */
#ifndef BBOS_GPIO_NUMBER_OF_PINS
#define BBOS_GPIO_NUMBER_OF_PINS 256
#endif

struct bbos_gpio_chip {
	char *label;
	int base; // the very first pin number
	unsigned int n; // the number of pins handled by this chip
};

struct bbos_gpio_pin {
	struct bbos_gpio_chip *chip; // chip to which this pin belongs
	bbos_thread_id_t owner; // thread which owns this pin
};

extern struct bbos_gpio_pin bbos_gpio_table[BBOS_GPIO_NUMBER_OF_PINS];

#define bbos_gpio_pin_to_chip(pin) bbos_gpio_table[pin].chip

enum bbos_gpio_commands {
	BBOS_GPIO_OPEN,		// replacement for BBOS_DRIVER_OPEN
	BBOS_GPIO_CLOSE,	// replacement for BBOS_DRIVER_CLOSE
	BBOS_GPIO_DIRECTION_INPUT,
	BBOS_GPIO_DIRECTION_OUTPUT,
	BBOS_GPIO_SET_VALUE,
	BBOS_GPIO_GET_VALUE
};

struct bbos_gpio_message {
	unsigned int pin;
	unsigned int value;
};

bbos_return_t bbos_gpio_register_chip(struct bbos_gpio_chip *chip);

bbos_return_t bbos_gpio_unregister_chip(struct bbos_gpio_chip *chip);

#endif /* __BBOS_GPIO_DRIVER_H */


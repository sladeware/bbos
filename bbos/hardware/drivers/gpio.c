/*
 * Optional implementation driver for GPIO interfaces.
 *
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

#include <bbos.h>
#include <bbos/hardware/drivers/gpio.h>

struct bbos_gpio_pin bbos_gpio_table[BBOS_GPIO_NUMBER_OF_PINS];

/**
 * bbos_gpio_register_chip - Register gpio_chip chip.
 * @chip: The chip to register, with chip->base initialized.
 */
bbos_return_t
bbos_gpio_register_chip(struct bbos_gpio_chip *chip)
{
	unsigned int id;
	int base;

	base = chip->base;

	/* Trace GPIO numbers so they must not be managed by another GPIO chip */
	for (id=base; id<(base + chip->n); id++) {
		if (bbos_gpio_table[id].chip != NULL) {
			return BBOS_BUSY;
		}		
	}

	for (id=base; id<(base + chip->n); id++) {
		bbos_gpio_table[id].chip = chip;
		bbos_gpio_table[id].owner = BBOS_UNKNOWN_ID;
	}
	
	return BBOS_SUCCESS;
}

/**
 * bbos_gpio_unregister_chip
 * @chip: The chip to unregister.
 */
bbos_return_t
bbos_gpio_unregister_chip(struct bbos_gpio_chip *chip)
{
	unsigned int id;
	int base;

	base = chip->base;

	for (id=base; id<(base + chip->n); id++) {
		bbos_gpio_table[id].chip = NULL;
		bbos_gpio_table[id].owner = BBOS_UNKNOWN_ID;
	}

	return BBOS_SUCCESS;
}



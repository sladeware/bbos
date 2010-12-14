/*
 * Optional implementation driver library for GPIO interfaces.
 *
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

#include <bbos/drivers/gpio/libgpio.h>

struct gpio_pin gpio_table[GPIO_NUMBER_OF_PINS];

/**
 * gpio_register_chip - Register gpio_chip chip.
 * @chip: The chip to register, with chip->base initialized.
 */
int16_t
gpio_register_chip(struct gpio_chip *chip)
{
  uint16_t id;
  int16_t base;

  base = chip->base;

  /* Trace GPIO numbers so they must not be managed by another GPIO chip */
  for (id=base; id<(base + chip->n); id++) {
    if (gpio_table[id].chip != NULL) {
      return 1;
    }		
  }

  for (id=base; id<(base + chip->n); id++) {
    gpio_table[id].chip = chip;
    gpio_table[id].owner = -1;
  }
	
  return 0;
}

/**
 * gpio_unregister_chip
 * @chip: The chip to unregister.
 */
int16_t
gpio_unregister_chip(struct gpio_chip *chip)
{
  uint16_t id;
  int16_t base;

  base = chip->base;
  
  for (id=base; id<(base + chip->n); id++) {
    gpio_table[id].chip = NULL;
    gpio_table[id].owner = -1;
  }

  return 0;
}



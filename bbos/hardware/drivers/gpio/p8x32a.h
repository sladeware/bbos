/*
 * P8X32A GPIO driver.
 *
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

#ifndef __P8X32A_GPIO_H
#define __P8X32A_GPIO_H

#define BBOS_GPIO_NUMBER_OF_PINS 32

#include <bbos/hardware/drivers/gpio.h>

void p8x32a_gpio_init();

#endif /* __P8X32A_GPIO_H */


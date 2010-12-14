/*
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

#ifndef __P8X32A_GPIO_H
#define __P8X32A_GPIO_H

#include <stdio.h>
#include <bbos/kernel.h>
#include <bbos/drivers/gpio/libgpio.h>

void p8x32a_gpio_init(bbos_thread_id_t id, bbos_port_id_t port);
void p8x32a_gpio_messenger();

#endif



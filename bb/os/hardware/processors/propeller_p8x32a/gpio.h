/**
 * @file bb/os/drivers/gpio/p8x32_gpio.h
 * @brief Propeller P8X32 GPIO driver
 */

/*
 * Copyright (c) 2011 Sladeware LLC
 */
#ifndef __P8X32_GPIO_H
#define __P8X32_GPIO_H

#include <bb/os/drivers/gpio/core.h>

#ifndef __CATALINA__
#error "This implementation requires Catalina compiler."
#endif

GPIO_DRIVER_INTERFACE_PROTO(p8x32);

#endif /* __P8X32_GPIO_H */

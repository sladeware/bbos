/*
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko                                                      */

#ifndef __BBOS_H
#define __BBOS_H

#include <bbos/compiler.h>

/* Thread IDs */
#define GPIO_DRIVER 0
#define MOVE 1

/* The number of BBOS application threads */
#define BBOS_NUMBER_OF_APPLICATION_THREADS 2

/* Application switcher macro */
#define bbos_application_switcher(id)		\
  switch(id) {					\
  case GPIO_DRIVER:				\
    gpio_driver();				\
    break;					\
  case MOVE:					\
    move();					\
    break;					\
  default:					\
    bbos_exit()					\
  }						\

/* Port IDs */
#define GPIO_DRIVER_PORT 0
#define MOVE_PORT 1

/* The number of ports in this process */
#define BBOS_NUMBER_OF_PORTS 2

/* BBOS Driver Constants */
#define GPIO_DRIVER_NAME "gpio_driver"
#define GPIO_DRIVER_VERSION 2

#include <bbos/kernel.h>

#endif /* __BBOS_H */


/*
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_H
#define __BBOS_H

#include <bbos/compiler.h>

/* Thread IDs */
#define MOVE 0
#define BBOS_IDLE 1
#define BBOS_IPC 2
#define GPIO 3

/* The number of BBOS application threads */
#define BBOS_NUMBER_OF_APPLICATION_THREADS 4

/* Application static scheduler macro */
#define BBOS_SCHEDULER_STATIC
#define bbos_static_scheduler()  \
  while(true) { \
    move(); \
    bbos_idle(); \
    bbos_ipc(); \
    gpio_driver_main(); \
  }

/* Port IDs */
#define FINGER_PORT 0
#define GPIO_DRIVER_PORT 1

/* The number of ports in this process */
#define BBOS_NUMBER_OF_PORTS 2

/* Mempool IDs */

/* The number of mempools in this process */
#define BBOS_NUMBER_OF_MEMPOOLS 0

/* BBOS driver constants */
#define GPIO_DRIVER_NAME "gpio"
#define GPIO_DRIVER_VERSION 2

/* BBOS driver bootstrapper functions */
#define bbos_boot_drivers \
    gpio_driver_init(); \

/* BBOS driver exit functions */
#define bbos_exit_drivers \
    gpio_driver_exit(); \

/* The include files we are using  */
#include <propeller_demo_board.h>

#include <bbos/kernel.h>

#endif /* __BBOS_H */

/*
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_PROCESS_H
#define __BBOS_PROCESS_H

#ifdef __cplusplus
extern "C" {
#endif

#include <bbos/kernel/process/thread.h>
#include <bbos/kernel/process/sched.h>
#include <bbos/kernel/process/port.h>

/*
 * If the number of ports was not defined, it equals 0.
 */
#ifndef BBOS_NUMBER_OF_PORTS
#define BBOS_NUMBER_OF_PORTS 0
#endif /* BBOS_NUMBER_OF_PORTS */

/*
 * The number of ports can be equal zero, but can not be great
 * than BBOS_MAX_NUMBER_OF_PORTS.
 */
#if BBOS_NUMBER_OF_PORTS > 0
extern bbos_port_t bbos_process_port_table[BBOS_NUMBER_OF_PORTS];
#endif /* BBOS_NUMBER_OF_PORTS */
#if BBOS_NUMBER_OF_PORTS > BBOS_MAX_NUMBER_OF_PORTS
#error "BBOS_NUMBER_OF_PORTS > BBOS_MAX_NUMBER_OF_PORTS"
#endif /* BBOS_NUMBER_OF_PORTS > BBOS_MAX_NUMBER_OF_PORTS */

/*
 * If the number of device drivers was not defined, it equals 0.
 */
#ifndef BBOS_NUMBER_OF_DEVICE_DRIVERS
#define BBOS_NUMBER_OF_DEVICE_DRIVERS 0
#endif /* BBOS_PROCESS_NUMBER_OF_DEVICE_DRIVERS */

/*
 * The number of device drivers can be equal to zero, but can not
 * be great than BBOS_MAX_NUMBER_OF_DEVICE_DRIVERS.
 */
#if BBOS_NUMBER_OF_DEVICE_DRIVERS > 0
extern bbos_device_driver_t bbos_process_device_driver_table[BBOS_NUMBER_OF_DEVICE_DRIVERS];
#endif /* BBOS_NUMBER_OF_DEVICE_DRIVERS > 0 */

#if BBOS_NUMBER_OF_DEVICE_DRIVERS > BBOS_MAX_NUMBER_OF_DEVICE_DRIVERS
#error "BBOS_NUMBER_OF_DEVICE_DRIVERS > BBOS_MAX_NUMBER_OF_DEVICE_DRIVERS"
#endif /* BBOS_NUMBER_OF_DEVICE_DRIVERS > BBOS_MAX_NUMBER_OF_DEVICE_DRIVERS */

/*
 * The number of threads should be greater than 0, but
 * less than BBOS_MAX_NUMBER_OF_THREADS.
 */
#if BBOS_NUMBER_OF_THREADS == 0
#error "BBOS_NUMBER_OF_THREADS must be >0"
#endif /* BBOS_NUMBER_OF_THREADS == 0 */
#if BBOS_NUMBER_OF_THREADS > BBOS_MAX_NUMBER_OF_THREADS
#error "BBOS_NUMBER_OF_THREADS > BBOS_MAX_NUMBER_OF_THREADS"
#endif /* BBOS_NUMBER_OF_THREADS > BBOS_MAX_NUMBER_OF_THREADS */

extern bbos_thread_t bbos_process_thread_table[BBOS_NUMBER_OF_THREADS];

/* Prototypes */

void bbos_process_init();

void bbos_process_test();

void bbos_process_start();

void bbos_process_stop();

#ifdef __cplusplus
}
#endif

#endif /* __BBOS_PROCESS_H */



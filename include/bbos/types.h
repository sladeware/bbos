/*
 * The BBOS specific data types.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_TYPES_H
#define __BBOS_TYPES_H

/* Load portable compiler specific data types */
#include <bbos/lib/stdint.h>
#include <bbos/lib/stddef.h>
#include <bbos/lib/stdbool.h>

/**
 * typedef bbos_port_id_t - Port identifier.
 */typedef uint8_t bbos_port_id_t;
#define BBOS_MAX_NUMBER_OF_PORTS UINT8_MAX

/**
 * typedef bbos_thread_id_t - Type of the thread identifier.
 */
typedef uint16_t bbos_thread_id_t;
#define BBOS_MAX_NUMBER_OF_THREADS UINT8_MAX

/**
 * typedef bbos_thread_priority_t - Type of thread priority.
 */
typedef uint8_t bbos_thread_priority_t;
#define BBOS_THREAD_MAX_PRIORITY_VALUE UINT8_MAX

/**
 * typedef bbos_return_t - Type of the BBOS code.
 */
typedef int16_t bbos_return_t;

#endif /* __BBOS_TYPES_H */

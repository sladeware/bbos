/*
 * Global type definitions.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_TYPES_H
#define __BBOS_TYPES_H

/* Load portable compiler specific data types */
#include <bbos/lib/portable_stdint.h>

typedef struct {
  uint8_t b[8]; // b - byte
} uint64_t;

typedef struct {
  int8_t b[8]; // b - byte
} int64_t;

/**
 * typedef bbos_port_id_t - Port identifier.
 */
typedef uint8_t bbos_port_id_t;
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

//#ifndef NULL
//#define NULL (0)
//#endif

#ifndef FALSE
#define FALSE 0
#endif

#ifndef TRUE
#define TRUE (!FALSE)
#endif

#endif /* __BBOS_TYPES_H */

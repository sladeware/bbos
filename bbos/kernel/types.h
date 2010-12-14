/*
 * This header file contains important data type definitions. It is considered 
 * good programming practice to use these definitions, instead of the underlying
 * base type. By convention, all type names have postfix _t.
 *
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_TYPES_H
#define __BBOS_TYPES_H

#include <limits.h>

#ifdef HAVE_INTTYPES_H
#include <inttypes.h>
#endif

#ifdef HAVE_STDINT_H
#include <stdint.h>
#endif

//#ifdef HAVE_STDDEF_H
#include <stddef.h>
//#endif

/* 
 * The type size_t holds all results of the sizeof operator.  At first glance,
 * it seems obvious that it should be an unsigned int, but this is not always 
 * the case. 
 */
#ifndef _SIZE_T
#define _SIZE_T
typedef unsigned int size_t;
#endif

/*
 * The type ssize_t is the signed version of size_t.
 */
#ifndef _SSIZE_T
#define _SSIZE_T
typedef int ssize_t;
#endif

typedef char int8_t; // ! signed
typedef unsigned char uint8_t;
typedef signed short int16_t;
typedef unsigned short uint16_t;
typedef signed int int32_t;
typedef unsigned int uint32_t;

typedef long long uint64_t;

typedef unsigned char bool_t;

typedef int32_t bbos_return_t;

typedef int16_t bbos_thread_id_t;

typedef int16_t bbos_port_id_t;

#define FALSE 0
#define TRUE (!FALSE)

#endif


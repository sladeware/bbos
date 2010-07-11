/*
 * stdint.h header file.
 *
 * The naming convention for exact-width integer types is intN_t for signed 
 * integers and uintN_t for unsigned integers. Additionally their ranges are
 * defined as INTN_MIN, INTN_MAX and UINTN_MIN, UINTN_MAX.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_LIB_STDINT_H
#define __BBOS_LIB_STDINT_H

#include <limits.h>

#ifndef SIZE_MAX
#define SIZE_MAX (~(size_t) 0)
#endif /* SIZE_MAX */

/*
 * Deduce the type assignments from limits.h under the assumption that
 * integer sizes in bits are powers of 2, and follow the ANSI
 * definitions.
 */

#ifndef UINT8_MAX
#define UINT8_MAX 0xff
#endif /* UINT8_MAX */
#ifndef uint8_t
#if(UCHAR_MAX == UINT8_MAX)
typedef unsigned char uint8_t;
#define UINT8_C(v) ((uint8_t) v)
#else
#error "Platform not supported"
#endif
#endif /* uint8_t */

#ifndef INT8_MAX
#define INT8_MAX 0x7f
#endif /* INT8_MAX */
#ifndef INT8_MIN
#define INT8_MIN INT8_C(0x80)
#endif /* INT8_MIN */
#ifndef int8_t
#if(SCHAR_MAX == INT8_MAX)
typedef signed char int8_t;
#define INT8_C(v) ((int8_t) v)
#else
#error "Platform not supported"
#endif
#endif /* int8_t */

#ifndef UINT16_MAX
#define UINT16_MAX 0xffff
#endif
#ifndef uint16_t
#if(UINT_MAX == UINT16_MAX)
typedef unsigned int uint16_t;
#define UINT16_C(v) ((uint16_t) (v))
#elif(USHRT_MAX == UINT16_MAX)
typedef unsigned short uint16_t;
#define UINT16_C(v) ((uint16_t) (v))
#else
#error "Platform not supported"
#endif
#endif

#ifndef INT16_MAX
#define INT16_MAX 0x7fff
#endif /* INT16_MAX */
#ifndef INT16_MIN
#define INT16_MIN INT16_C(0x8000)
#endif /* INT16_MIN */
#ifndef int16_t
#if(INT_MAX == INT16_MAX)
typedef signed int int16_t;
#define INT16_C(v) ((int16_t) (v))
#elif(SHRT_MAX == INT16_MAX)
typedef signed short int16_t;
#define INT16_C(v) ((int16_t) (v))
#else
#error "Platform not supported"
#endif
#endif /* int16_t */

#ifndef UINT32_MAX
#define UINT32_MAX (0xffffffffUL)
#endif /* UINT32_MAX */
#ifndef uint32_t
#if(ULONG_MAX == UINT32_MAX)
typedef unsigned long uint32_t;
#define UINT32_C(v) v ## UL
#elif (UINT_MAX == UINT32_MAX)
typedef unsigned int uint32_t;
#define UINT32_C(v) v ## U
#elif (USHRT_MAX == UINT32_MAX)
typedef unsigned short uint32_t;
#define UINT32_C(v) ((unsigned short) (v))
#else
#error "Platform not supported"
#endif
#endif /* uint32_t */

#ifndef INT32_MAX
#define INT32_MAX (0x7fffffffL)
#endif /* INT32_MAX */
#ifndef INT32_MIN
#define INT32_MIN INT32_C(0x80000000)
#endif
#ifndef int32_t
#if(LONG_MAX == INT32_MAX)
typedef signed long int32_t;
#define INT32_C(v) v ## L
#elif (INT_MAX == INT32_MAX)
typedef signed int int32_t;
#define INT32_C(v) v
#elif (SHRT_MAX == INT32_MAX)
typedef signed short int32_t;
#define INT32_C(v) ((short) (v))
#else
#error "Platform not supported"
#endif
#endif /* int32_t */

/*
typedef struct {
  uint8_t b[8]; // b - byte
} uint64_t;

typedef struct {
  int8_t b[8]; // b - byte
} int64_t;
*/

#endif /* __BBOS_LIB_PORTABLE_STDINT_H */



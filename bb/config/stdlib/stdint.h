/*
 * A portable <stdint.h> header file
 *
 * Copyright (c) 2011 Sladeware LLC
 */

#ifndef __BB_STDINT_H
#define __BB_STDINT_H

#include <bb/config.h>

#if defined(BB_HAS_STDINT_H)
# include <stdint.h>
#else /* defined(BB_HAS_STDINT_H) */

#include <limits.h>

// 8-bit types
#if UCHAR_MAX == 0xFF
typedef char int8_t;
typedef unsigned char uint8_t;
#else
# error Defaults not correct; please hand modify bb/stdint.h
#endif

/*
 * 16-bit types
 */
#if USHRT_MAX == 0xFFFF
typedef short int16_t;
typedef unsigned short uint16_t;
#else
# error "Defaults not correct; please hand modify bb/stdint.h"
#endif
/*
 * 32-bit types
 */
#if ULONG_MAX == 0xFFFFFFFF
typedef long int32_t;
typedef unsigned long uint32_t;
#elif UINT_MAX == 0xFFFFFFFF
typedef signed int int32_t;
typedef unsigned int uint32_t;
#else
# error "Defaults not correct; please hand modify bb/stdint.h"
#endif
/*
 * 64-bit types
 */
#if defined(BB_HAS_LONG_LONG)
typedef long long uint64_t;
#else
# error Defaults not correct; please hand modify bb/config/stdlib/stdint.h
#endif /* defined(BB_HAS_LONG_LONG) */
/*
 * Boolean type with values TRUE and FALSE.
 */
typedef unsigned char bool_t;

#endif /* defined(BB_HAS_STDINT_H) */

#endif /* __BB_STDINT_H */

/*
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_LOG2_H
#define __BBOS_LOG2_H

#include <bbos/kernel/types.h>

/**
 * is_power_of_2 - Determine whether some value is a power of two.
 * @n: Parameter.
 *
 * Note:
 *
 * Zero is _not_ considered a power of two.
 */
static bool_t 
is_power_of_2(uint32_t n)
{
	return (n != 0 && ((n & (n - 1)) == 0));
}

/**
 * __roundup_pow_of_two - Round up to nearest power of two.
 * @n: Parameter.
 */
static uint32_t
__roundup_pow_of_2(uint32_t n)
{
	return 1UL << 1;//fls_long(n - 1);
}

/**
 * __rounddown_pow_of_2 - Round down to nearest power of two.
 * @n: Parameter.
 */
static uint32_t
__rounddown_pow_of_2(uint32_t n)
{
	n |= (n >> 1); 
	n |= (n >> 2); 
	n |= (n >> 4); 
	n |= (n >> 8); 
	n |= (n >>16); 
	return n - (n >> 1); 
}

/**
 * rounddown_pow_of_two - Round the given value down to nearest power of two.
 * @n: Parameter
 *
 * Note:
 *
 * The result is undefined when n is 0.
 */
#define rounddown_pow_of_2(n)	\
	(	\
		__rounddown_pow_of_2(n)		\
	)

static const int16_t mult_de_bruijn_bit_pos2[32] = {
  0, 1, 28, 2, 29, 14, 24, 3, 30, 22, 20, 15, 25, 17, 4, 8, 
  31, 27, 13, 23, 21, 19, 16, 7, 26, 12, 18, 6, 11, 5, 10, 9
};

int16_t
__ilog2_32(uint32_t n)
{
	return mult_de_bruijn_bit_pos2[(uint32_t)(n * 0x077CB531U) >> 27];
}

int16_t
__ilog2_64(uint64_t n)
{
	return 0; // TODO
}

/**
 * ilog2 - Log of base 2 of 32-bit or a 64-bit unsigned value.
 * @n: Parameter
 */
#define ilog2(n) \
	(sizeof(n) <= 4) ?	\
	__ilog2_32(n) :			\
	__ilog2_64((uint64_t)n)				\

#endif /* __BBOS_LOG2_H */


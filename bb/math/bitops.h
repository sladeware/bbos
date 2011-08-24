/*
 * Copyright (c) 2011 Sladeware LLC
 */

/**
 * @file bb/math/bitops.h
 * @brief Bit operations
 */

#ifndef __BBOS_MATH_BITOPS_H
#define __BBOS_MATH_BITOPS_H

#define BIT(n)                                  \
  (1UL << (n))

#define rol32(word, shift)                      \
  ((word << shift) | (word >> (32 - shift)));

#endif /* __BBOS_MATH_BITOPTS_H */


/**
 * @file bitops.h
 * @brief Bit operations
 */

#ifndef __BBOS_BITOPS_H
#define __BBOS_BITOPS_H

#define BIT(nr) (1UL << (nr))

#define rol32(word, shift)				\
  ((word << shift) | (word >> (32 - shift)));

#endif


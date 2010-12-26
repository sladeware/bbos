/*
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_BITOPS_H
#define __BBOS_BITOPS_H

/**
 * rol32 - rotate a 32-bit value left
 * @word: value to rotate
 * @shift: bits to roll
 */
 
//static unsigned rol32(unsigned word, unsigned shift)
#define rol32(word, shift) \
	((word << shift) | (word >> (32 - shift)));

#endif


/*
 * Additional string routines.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#include <stddef.h>
#include <bbos/lib/bbos_string.h>

/**
 * xtoa - Convert hex string to char string and returns length of decoded
 * string.
 * @s: Pointer to the source hex string.
 * @d: Pointer to the destination char string.
 *
 * Return value:
 *
 * Length of the destination string.
 */
int16_t
xtoa(uint8_t* s, uint8_t* d)
{
  size_t l;
  int16_t i, x;

  l = strlen(s);

  for(i=l>>1; i>=0; i--) {
    *(d+i) = 0;
  }

  for(i=l; i>=0; i--) {
    if(*(s+i) >= 97) {
      x = *(s+i) - 87; /* 97 + 10 */
    }
    else if(*(s+i) >= 65) {
      x = *(s+i) - 55; /* 65 + 10 */
    }
    else {
      x = *(s+i) - 48;
    }
    *(d+(i>>1)) += ((i&1) ? 1 : 16) * x;
  }

  return (l>>1);
}




#include "bitwise_op.h"

int
muxc(int dest, int mask, char c)
{
  if (c)
    return dest | mask;
  return dest & ~mask;
}

char
parity(int x)
{
  x = x ^ (x >> 1);
  x = (x ^ (x >> 2)) & 0x11111111;
  x = x * 0x11111111;
  return (x >> 28) & 1;
}

int
ror(int x, int bits)
{
  int lsb = 0;
  while (bits)
    {
      bits--;
      lsb = x & 0x1;
      x >>= 1;
      x |= lsb << 31;
    }
  return x;
}

/**
 * Right rotate through carry.
 *
 * @param c Carry flag
 *
 * http://en.wikipedia.org/wiki/Bitwise_operation#Rotate_through_carry
 */
int
rcr(int x, int bits, char c)
{
  int lsb = 0;
  while (bits)
    {
      bits--;
      lsb = x & 0x1;
      x >>= 1;
      x |= c << 31;
      c = lsb;
    }
  return x;
}

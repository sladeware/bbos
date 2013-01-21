/*
 * Copyright (c) 2012 Sladeware LLC
 *
 * Author: Oleksandr Sviridenko
 */

#include "time.h"
#include "core.h"

#define NR_COGS 8

void
occupy_cog(void)
{
  do {} while (1);
}

#ifdef __CATALINA__

// @see detect_free_cogs().
char
count_free_cogs()
{
  char c;
  c = detect_free_cogs();
  c -= (c >> 1) & 0x55555555;
  c = (c & 0x33333333) + ((c >> 2) & 0x33333333);
  c = (c + (c >> 4)) & 0x0F0F0F0F;
  c += c >> 8;
  c += c >> 16;
  return c & 0x0000003F;
}

/**
 * Returns bitset of free cogs, where each free cog is marked as 1.
 */
int
detect_free_cogs()
{
  unsigned long stacks[4 * NR_COGS];
  int bitset = 0;
  char i;
  int cog_no;

  for (i = 0; i < NR_COGS; i++)
    {
      // Many thanks to Ross for fixing a bug.
      cog_no = _coginit_C(&occupy_cog, &stacks[4 * (i + 1)]);
      if (cog_no < 0) // if no more cogs left then break
        {
          break;
        }
      else
        {
          bitset |= (1 << cog_no);
        }
    }
  // Free occupied cogs
  for (i = 0; i < NR_COGS; i++)
    {
      if ((bitset & (1 << i)) > 0)
        {
          _cogstop(i);
        }
    }

  return bitset;
}

#endif /* __CATALINA__ */

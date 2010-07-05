/*
 * Delay routines.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#include <bbos/lib/delay.h>

/**
 * sdelay - Delay on a period in seconds.
 * @delay: Delay in seconds.
 */
void
sdelay(uint32_t delay)
{
  uint32_t time0;

//  for (time0 = SEC_TIMER; (SEC_TIMER - time0) < delay;);
}

/**
 * Delay on a period in milliseconds.
 * @delay: Delay in miliseconds.
 */
void
mdelay(uint32_t delay)
{
  uint32_t time0;

//  for (time0 = MS_TIMER; (MS_TIMER - time0) < delay;);
}


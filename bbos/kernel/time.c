/*
 * Delay routines.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#include <bbos.h>

/**
 * bbos_delay_sec - Delay on a period in seconds.
 * @delay: Delay in seconds.
 */
void
bbos_delay_sec(uint32_t delay)
{
  uint32_t time0;

//  for (time0 = SEC_TIMER; (SEC_TIMER - time0) < delay;);
}

/**
 * bbos_delay_msec - Delay on a period in milliseconds.
 * @delay: Delay in miliseconds.
 */
void
bbos_delay_msec(uint32_t delay)
{
  uint32_t time0;

//  for (time0 = MS_TIMER; (MS_TIMER - time0) < delay;);
}

/**
 * bbos_delay_usec - Delay on a period in microseconds.
 * @delay: Delay in microseconds.
 */
void
bbos_delay_usec(uint32_t delay)
{
}




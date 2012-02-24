/*
 * Copyright (c) 2012 Sladeware LLC
 */
#include <bb/os/drivers/processors/propeller_p8x32/delay.h>

#ifdef __CATALINA__

void
bbos_delay_usec(int usecs)
{
  _waitcnt(_cnt() + usecs * (_clockfreq() / 1000000));
}

#elif defined(__GNUC__)
#include <propeller.h>

void
bbos_delay_msec(int msec)
{
  waitcnt((CLKFREQ / 1000) * msec + CNT);
}

void
bbos_delay_usec(int usec)
{
  if(usec < 10) /* very small t values will cause a hang */
    return; /* don't bother function delay is likely enough */
  waitcnt((CLKFREQ / 1000000) * usec + CNT);
}
#endif /* no errors */

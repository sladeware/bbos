/*
 * Copyright (c) 2012 Sladeware LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#include <bb/os/drivers/processors/propeller_p8x32/delay.h>
#include <bb/os/drivers/processors/propeller_p8x32/sio.h>
#ifdef __CATALINA__

void
bbos_delay_usec(int usecs)
{
  _waitcnt(_cnt() + usecs * (_clockfreq() / 1000000));
}

#elif defined(__GNUC__)

#include <sys/thread.h>

void
bbos_delay_msec(int msec)
{
#if 0 /* XXX: version for threading support. See __naputil(). */
  unsigned waitcycles;
  unsigned msecond = propeller_get_clockfreq() / 1000;

  waitcycles = propeller_get_cnt() + msec * msecond;
  __napuntil(waitcycles);
  
#else
  BBOS_DELAY_MSEC(msec);
#endif
}

void
bbos_delay_usec(int usec)
{
  if(usec < 10) /* very small t values will cause a hang */
    return; /* don't bother function delay is likely enough */
  waitcnt((CLKFREQ / 1000000) * usec + CNT);
}
#endif /* no errors */

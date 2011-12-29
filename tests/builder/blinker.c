/*
 * This test blinks specified LED.
 *
 * Copyright (c) 2011 Sladeware LLC
 */

#ifndef LED
#error LED has to be defined manually
#endif

#include <catalina_cog.h>
#include <stdio.h>

static int mask = 1 << LED;
static int on_off = 1 << LED;

#define DELAY_SEC(seconds) \
  _waitcnt(_cnt() + (seconds * _clockfreq()) - 4296)

void
blink_an_led()
{
  _dira(1 << LED, on_off);
  _outa(1 << LED, on_off);
  DELAY_SEC(3);
  on_off ^= mask;
}

int
main()
{
  while (1)
    {
      blink_an_led();
    }
  return 0;
}

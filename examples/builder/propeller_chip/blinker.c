/*
 * This test blinks specified LED.
 *
 * Copyright (c) 2012 Sladeware LLC
 */

#ifndef LED
#error LED has to be defined manually
#endif

/* Set default delays */
#ifndef DELAY
#define DELAY 1 /* seconds */
#endif
#define PROMPT_DELAY 50 /* mseconds */

#include <catalina_cog.h>
#include <stdio.h>

static int mask = 1 << LED;
static int on_off = 1 << LED;

#define MAKE_DELAY(msec) \
  _waitcnt(_cnt() + ((msec) * (_clockfreq() / 1000)) - 4296)

void
blink_an_led()
{
  _dira(1 << LED, on_off);
  _outa(1 << LED, on_off);
  MAKE_DELAY(1 * 1000);
  on_off ^= mask;
}

int
main()
{
  /* Initialize LEDs */
  unsigned i;
  for (i = 16; i < 24; i++)
    {
      _dira(1 << i, 1 << i);
      _outa(1 << i, 1 << i);
      MAKE_DELAY(PROMPT_DELAY);
    }
  for (i = 16; i < 24; i++)
    {
      _outa(1 << i, 0);
      MAKE_DELAY(PROMPT_DELAY);
    }

  /* Blink an LED forever... */
  while (1)
    {
      blink_an_led();
    }

  return 0;
}

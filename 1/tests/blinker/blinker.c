/*
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

#include <bb/os/config.h>
#include BBOS_FIND_PROCESSOR_FILE(delay.h)

#include <stdio.h>

#define GET_PIN(p) (1<<p)

static int mask = GET_PIN(__CATALINA_LED);
static int on_off = GET_PIN(__CATALINA_LED);

void
blink_runner()
{
	_dira(mask, on_off);
  _outa(mask, on_off);
  bbos_delay_sec(3);
  on_off ^= mask;
}

int
main()
{
	while (1) {
	  blink_runner();
	}
	
  return 0;
}


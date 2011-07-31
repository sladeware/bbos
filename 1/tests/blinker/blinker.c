/*
 * Copyright (c) 2011 Sladeware LLC
 */

#include <bb/os/config.h>
#include <bb/os/kernel/system.h>

#include BBOS_FIND_PROCESSOR_FILE(delay.h)
#include BBOS_FIND_PROCESSOR_FILE(gpio.h)

#include <stdio.h>

static int mask = GET_PIN(__CATALINA_LED);
static int on_off = GET_PIN(__CATALINA_LED);

void
blink_runner()
{
	GPIOA_SET_DIRECTION(__CATALINA_LED, on_off);
  GPIOA_SET_VALUE(__CATALINA_LED, on_off);
  bbos_delay_sec(3);
  on_off ^= mask;
}

int
main()
{
  bbos_init();
  bbos_add_thread(BLINK, blink_runner);
  bbos_start();

  return 0;
}


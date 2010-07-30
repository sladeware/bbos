/*
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

//#include <stddef.h>
//#include <stdio.h>
#include <bbos.h>

#include <catalina_cog.h>

unsigned count;
unsigned on_off = 1;

void
blink_led(unsigned led) {
  //_outa(1<<led, (1<<led)*on_off);
  //count += 6250000;
  //_waitcnt(count);

  if(led == 23) {
    on_off ^= 1;
  }
}

bbos_return_t
led_switcher(bbos_thread_id_t tid)
{
  switch(tid) {
  case LED16_ID: blink_led(16); break;
  case LED17_ID: blink_led(17); break;
  case LED18_ID: blink_led(18); break;
  case LED19_ID: blink_led(19); break;
  case LED20_ID: blink_led(20); break;
  case LED21_ID: blink_led(21); break;
  case LED22_ID: blink_led(22); break;
  case LED23_ID: blink_led(23); break;
  }

  return BBOS_SUCCESS;
}

int
main(void)
{
  unsigned int i;

  for(i=16; i<24; i++) {
    _dira(1<<i, 1<<i);
  }

  count = _cnt();


  bbos_init();

  bbos_thread_start(LED16_ID);
  bbos_thread_start(LED17_ID);
  bbos_thread_start(LED18_ID);
  bbos_thread_start(LED19_ID);
  bbos_thread_start(LED20_ID);
  bbos_thread_start(LED21_ID);
  bbos_thread_start(LED22_ID);
  bbos_thread_start(LED23_ID);
  bbos_start();

  return 0;
}


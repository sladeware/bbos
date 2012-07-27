/*
 * Copyright (c) 2012 Sladeware LLC
 */
#include "cog.h"
#include "sio.h"
#include "time.h"

int
main()
{
    unsigned reg;
  unsigned LED_pin;

  while (1)
    {
      sio_printf("Hi, I'm cog#%d\n", cogid());
      delay_ms(100 * (cogid() + 1));
    }
  return 0;
}

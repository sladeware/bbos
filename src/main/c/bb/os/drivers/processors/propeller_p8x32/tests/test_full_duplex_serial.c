/*
 * Copyright (c) 2012 Sladeware LLC
 */
#include "full_duplex_serial.h"
#include "time.h"

int
main()
{
  while (1)
    {
      full_duplex_serial_open(31, 30, 0, 115200);
      full_duplex_serial_send_byte(65);
      delay_ms(500);
    }
  return 0;
}

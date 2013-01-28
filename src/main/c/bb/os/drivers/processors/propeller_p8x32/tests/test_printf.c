/*
 * Copyright (c) 2012 Sladeware LLC
 */

#include "cog.h"
#include "time.h"
#include "sio.h"

int
main()
{
  char *s;
  char c;
  int i;
  unsigned u;
  long int l;
  long unsigned n;
  unsigned x;

  sio_printf("%s", "\r\n*** sio_printf() test ***\r\n");

  sio_printf("Running cog         : %d\n", _cogid());
  sio_printf("Number of free cogs : %d\n\r", count_free_cogs());
  sio_printf("Mask of used cogs   : %d\n", detect_free_cogs());

  delay_ms(1000);

  s = "test";
  c = 'X';
  i = -12345;
  u =  12345;
  l = -1234567890;
  n =  1234567890;
  x = 0xABCD;

  sio_printf("-------------------------\r\n");

  sio_printf("string              : %s\r\n", s);
  sio_printf("char                : %c\r\n", c);
  sio_printf("integer             : %i\r\n", i);
  sio_printf("unsigned            : %u\r\n", u);
  sio_printf("long                : %l\r\n", l);
  sio_printf("unsigned long       : %n\r\n", n);
  sio_printf("hex                 : %x\r\n", x);
  sio_printf("multiple args       : %s %c %i %u %l %n %x\r\n",
             s, c, i, u, l, n, x);

  return 0;
}

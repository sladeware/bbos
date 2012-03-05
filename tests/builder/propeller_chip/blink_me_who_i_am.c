/*
 * The "Blink me who I am" test run on specified cog and flush
 * correspond LED on Propeller Demo Board.
 */
#include <propeller.h>
#include <bb/os/drivers/processors/propeller_p8x32/sio.h>

#define sleep_msec(msec) waitcnt((CLKFREQ / 1000) * msec + CNT);

int
main()
{
  _DIRA |= 0x00FF0000;

  //_OUTA = 1 << (16 + cogid());
  while (1)
    {
      /* Flush LED that corresponds to active cog. */
      DIRA &= 1 << (16 + cogid());
      OUTA &= 1 << (16 + cogid());
      sleep_msec(500); /* wait... */

      DIRA |= 1 << (16 + cogid());
      OUTA |= 1 << (16 + cogid());
      sleep_msec(500); /* wait... */

      sio_printf("I'm Cog #%d\n", cogid());
    }
  return 0;
}

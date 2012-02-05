/*
 * The "Blink me who I am" test run on specified cog and flush
 * correspond LED on Propeller Demo Board.
 */
#include <catalina_cog.h>
#include "time.h"

void
main()
{
  unsigned reg;
  unsigned led_mask;

#ifdef __CATALINA_DEMO
  led_mask = 1 << (_cogid() + 16);
#else /* __CATALINA_DEMO */
#error This board is not supported
#endif

  while (1)
    {
      /* Flush LED that corresponds to active cog. */
      reg = _dira(0, 0);
      _dira(reg ^ led_mask, reg ^ led_mask);
      reg = _outa(0, 0);
      _outa(reg ^ led_mask, reg ^ led_mask);
      delay_ms(1000);
    } /* wait... */
}

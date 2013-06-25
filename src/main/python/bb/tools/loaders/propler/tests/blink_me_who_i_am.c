/*
 * The "Blink me who I am" test run on specified cog and flush
 * correspond LED on Propeller Demo Board.
 */
#include <catalina_cog.h>
#include <catalina_icc.h>

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
      _dira(led_mask, (reg & led_mask) ^ led_mask);
      reg = _outa(0, 0);
      _outa(led_mask, (reg & led_mask) ^ led_mask);
      msleep(500); /* wait... */
    }
}

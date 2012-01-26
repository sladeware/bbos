/*
 * The "Who I am" test run on specified cog and flush
 * correspond LED on Propeller Demo Board.
 */
#include <catalina_cog.h>

void
main()
{
  unsigned reg;
  unsigned LED_pin;

  /* Initialization */
  //for (i = 16; i < 24; i++)
  //  {
  //    _dira(1 << i, 1 << i);
  //    _outa(1 << i, 0);
  //  }

  while (1) {
  /* Flush LED that corresponde to active cog. */
  LED_pin = 1 << (_cogid() + 16);
  reg = _dira(0, 0);
  _dira(reg | LED_pin, reg | LED_pin);
  reg = _outa(0, 0);
  _outa(reg | LED_pin, reg | LED_pin);
  } /* wait... */
}

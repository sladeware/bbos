
#include "time.h"

/*
 * Delay for a specified number of milliseconds.
 *
 * @ms: number of milliseconds
 */
void
delay_ms(int ms)
{
  _waitcnt(_cnt() + ms * (_clockfreq() / 1000));
}

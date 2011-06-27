
#include <catalina_cog.h>

void
bbos_delay_ms(int milliseconds)
{
  _waitcnt(_cnt() + (milliseconds * (_clockfreq() / 1000)) - 4296);
}

void
bbos_delay_sec(int seconds)
{
  bbos_delay_ms(seconds * 1000);
}


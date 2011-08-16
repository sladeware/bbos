/*
 * Copyright (c) 2011 Sladeware LLC
 */

#ifndef __CATALINA__
#error "This implementation requires Catalina compiler"
#endif

#include <catalina_cog.h>

void
bbos_sleep_ms(int milliseconds)
{
  _waitcnt(_cnt() + (milliseconds * (_clockfreq() / 1000)) - 4296);
}

void
bbos_sleep_sec(int seconds)
{
  bbos_sleep_ms(seconds * 1000);
}

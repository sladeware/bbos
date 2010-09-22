/*
 * Inter-thread communication.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#include <bbos.h>

void
bbos_itc_init()
{
#if BBOS_NUMBER_OF_PORTS > 0
  bbos_port_
#endif
}


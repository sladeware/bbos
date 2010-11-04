/*
 * Hardware support.
 *
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

#include <bbos.h>

void
bbos_hardware_init()
{
  printf("Initialize hardware\n");

  /* Initialize board */
#ifdef BBOS_BOARD
  printf("Initialize board\n");
#endif
}

void
bbos_hardware_exit()
{
}



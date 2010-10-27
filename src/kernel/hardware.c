/*
 * Hardware support.
 *
 * Copyright (c) ???? Slade Maurer, Alexander Sviridenko
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



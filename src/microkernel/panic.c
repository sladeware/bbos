/*
 * Panic handling.
 *
 * Copyright (C) 2010 Slade Maurer, Alexander Sviridenko
 */

#include <bbos/microkernel/panic.h>

/**
 * bbos_panic - Halt the system.
 * @fmt: The text string to print.
 *
 * Description:
 *
 * Display a message, then perform cleanups.
 *
 * Return value:
 *
 * This function should never return.
 */
void
bbos_panic(const uint8_t *fmt, ...)
{
  static uint8_t buf[128];
  va_list args;

  va_start(args, fmt);
  //vsnprintf(buf, sizeof(buf), fmt, args);
  va_end(args);

  printf("Panic: %s\n", buf);

  /* Exit with error */
  exit(1);
}


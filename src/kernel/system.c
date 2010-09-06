/*
 * BBOS.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#include <bbos.h>

/* The banner that gets printed on startup. */
const int8_t bbos_banner[] = "BBOS version " BBOS_VERSION_STR "\n";

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
bbos_panic(const char *fmt, ...)
{
  static char buf[128];
  va_list args;

  va_start(args, fmt);
  //vsnprintf(buf, sizeof(buf), fmt, args);
  va_end(args);

  printf("Panic: %s\n", buf);

  /* Exit with error */
  //exit(1);
}

/**
 * bbos_init - Main initialization.
 *
 * Note:
 *
 * The service must be called prior to calling bbos_start which will
 * actually start the system.
 */
void
bbos_init()
{
  printf("%s", bbos_banner);

  bbos_process_init();
}

/**
 * bbos_test - Test settings and components.
 */
void
bbos_test()
{
}

/**
 * bbos_start - Start BBOS.
 *
 * Return value:
 *
 * Never returns.
 */
void
bbos_start()
{
  bbos_test();
  bbos_process_start();
}

/**
 * bbos_stop - Stop BBOS.
 */
void
bbos_stop()
{
	exit(0);
}



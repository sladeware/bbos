/*
 * System.
 *
 * Copyright (c) ???? Slade Maurer, Alexander Sviridenko
 */

#include <bbos.h>

/* The banner that gets printed on startup. */
const int8_t bbos_banner[] = "BBOS version " BBOS_VERSION_STR "\n";

enum bbos_system_states bbos_system_state;

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
 * bbos_init - BBOS initialization.
 *
 * Note:
 *
 * The service must be called prior to calling bbos_start which will
 * actually start the system.
 */
void
bbos_init()
{
  /* BBOS_SYSTEM_BOOTING? */

  printf("%s", bbos_banner);

  /* Start the system initialization */
  bbos_system_state = BBOS_SYSTEM_INITIALIZATION;

  /* Initialize hardware */
  printf("Initialize hardware\n");
  bbos_hardware_init();

  printf("Initialize process\n");
  bbos_process_init();

  // Initialize inter-process communication here
  // bbos_ipc_init();
}

/**
 * bbos_test - Test settings and components.
 */
void
bbos_test()
{
  /* It seems to be fine */
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
  if (bbos_system_state != BBOS_SYSTEM_INITIALIZATION) {
    bbos_panic("BBOS was not initialized!\n");
  }

  /* Perform system test */
  bbos_system_state = BBOS_SYSTEM_TESTING;
  bbos_test();

  printf("Start process\n");
  bbos_system_state = BBOS_SYSTEM_RUNNING;
  bbos_process_start();
}

/**
 * bbos_stop - Stop BBOS.
 */
void
bbos_stop()
{
  /* Stop process */
  bbos_process_stop();

  exit(0);
}


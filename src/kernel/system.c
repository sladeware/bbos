/*
 * System.
 */

#include <bbos.h>

/* The banner that gets printed on startup. */
const int8_t bbos_banner[] = "BBOS version " BBOS_VERSION_STR "\n";

enum bbos_system_states bbos_system_state;

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
  /* Start the system initialization */
  bbos_system_state = BBOS_SYSTEM_INITIALIZATION;

  printf("%s", bbos_banner);

  bbos_hardware_init();
  bbos_process_init();

#ifdef BBOS_IPC
  bbos_ipc_init();
#endif
}

/**
 * bbos_test - Test settings and components.
 */
void
bbos_test()
{
  bbos_system_state = BBOS_SYSTEM_TESTING;

  printf("System testing\n");

  /* It seems to be fine */
}

void
bbos_exit()
{
  /* Do the application specific exit point first */
  bbos_application_exit();

#ifdef BBOS_IPC
  bbos_ipc_exit();
#endif

  exit(0);
}

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
  vsnprintf(buf, sizeof(buf), fmt, args);
  va_end(args);

  printf("Panic: %s\n", buf);

  /* Exit with error */
  bbos_exit();
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
  bbos_process_stop();
}

/**
 * bbos_main - Main entry point for the BBOS.
 *
 * Description:
 *
 * Called from main().
 *
 * Return value:
 *
 * Generic error code.
 */
bbos_return_t
bbos_main()
{
  /* Start entire system */
  bbos_init();

  /* Initialize application */
  bbos_application_init();

#ifdef BBOS_TEST
  /* Initiate system test */
  bbos_test();
#endif

  /* Start the system */
  bbos_start();

  return BBOS_SUCCESS;
}



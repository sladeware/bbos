/*
 * System control.
 *
 * Copyright (c) 2011 Sladem Maurer, Alexander Sviridenko
 */

#include <bbos/kernel.h>
#include <bbos/kernel/idle.h>
#include <stdio.h>

enum bbos_system_states bbos_system_state;

/**
 * bbos_banner - The banner that gets printed on startup.
 *
 * Description:
 *
 * Provides the very basic information about the system.
 */
void
bbos_banner()
{
  printf("BBOS version %s\n"
	 "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko\n",
	 BBOS_VERSION_STR);
}

/**
 * bbos_panic - Halt the system.
 * @fmt: The text string to print.
 *
 * Return value:
 *
 * The function should never return.
 *
 * Description:
 * 
 * Display a message, then perfom cleanups with exit.
 */
void
bbos_panic(const char *fmt, ...)
{
  static char buf[128];
  va_list args;
	
  va_start(args, fmt);
  // ???
  va_end(args);
	
  printf("Panic: %s\n", buf);
	
  //exit(0);
}

/**
 * bbos_init - Initialize BBOS.
 *
 * Description:
 *
 * Must be specified at the beginning of the program before calling any of the 
 * BBOS functions.
 */
void
bbos_init()
{
  /* Start the system initialization */
  bbos_system_state = BBOS_SYSTEM_INITIALIZATION;
	
  bbos_banner();
	
  printf("Initialize BBOS\n");
	
#ifndef	BBOS_DISABLE_SCHEDULER
  bbos_sched_init();
  bbos_thread_init(BBOS_IDLE_ID, bbos_idle, NULL);
#else
  printf("Scheduler was disabled.\n");
#endif /* BBOS_DISABLE_SCHEDULER */
}

/**
 * bbos_start - Start BBOS.
 */
void
bbos_start()
{
  if (bbos_system_state != BBOS_SYSTEM_INITIALIZATION
      && bbos_system_state != BBOS_SYSTEM_TESTING)
    {
      bbos_panic("BBOS was not initialized!\n");
    }
	
  // The system was initialized and we are ready to go!
  bbos_system_state = BBOS_SYSTEM_RUNNING;
	
  printf("Start BBOS\n");

  bbos();

#ifndef BBOS_DISABLE_SCHEDULER
  bbos_sched_do_loop();
#endif /* BBOS_DISABLE_SCHEDULER */
}

#ifdef BBOS_ENABLE_TESTING
/**
 * bbos_test - Test the settings and the system components.
 *
 * Description:
 *
 * The system test should not be critical so the system should run even if it 
 * fails. The test only provides the very basic information about system state,
 * and so it can stop it only if it's no signs of life.
 */
void
bbos_test()
{
  if (bbos_system_state != BBOS_SYSTEM_INITIALIZING) {
    bbos_panic("System was not initialized and so can not be tested\n");
  }
	
  bbos_system_state = BBOS_SYSTEM_TESTING;
	
  /* It seems to be fine now. */
}
#endif /* BBOS_ENABLE_TESTING */

/**
 * bbos_main - Main entry point for the BBOS system.
 *
 * Return value:
 *
 * Generic error code.
 *
 * Description:
 *
 * Basically called from main().
 */
bbos_return_t
bbos_main()
{
  /* Initialize system */
  bbos_init();
	
#ifdef BBOS_ENABLE_TESTING
  /* Initiate system test */
  bbos_test();
#endif
	
  /* Start up the system */
  bbos_start();
	
  return BBOS_SUCCESS;
}

// It's up to compiler to handle the main routine.
int
main()
{
  return bbos_main();
}



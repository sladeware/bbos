/*
 * Architecture independent initialization code.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#include <bbos.h>
#include BBOS_HARDWARE_ARCH_INC(init.h)

/* The banner that gets printed on startup. */
const int8_t bbos_banner[] = "BBOS version " BBOS_VERSION_STR "\n";

/**
 * bbos_init - Main initialization entry point.
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

  /* Basic architecture initialization */
  arch_init();

  /* Initialize target process */
  bbos_process_init();

  /* Initialize scheduler */
  bbos_sched_init();
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
 */
void
bbos_start()
{
  /* Test the system settings and components */
  bbos_test();

  /* Scheduling loop */
  while(1) {
    /* Try to schedule next thread */
    if(bbos_sched_next() != BBOS_SUCCESS) {
      break;
    }
  }

  bbos_panic("Scheduling terminated.\n");
}

/**
 * bbos_stop - Stop BBOS.
 */
void
bbos_stop()
{
}

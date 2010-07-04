/*
 * The BBOS microkernel system control.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#include <bbos/microkernel/sys.h>
#include BBOS_HARDWARE_ARCH_INC(arch_init.h)

/**
 * bbos_init - Main initialization service for microkernel.
 *
 * Note:
 *
 * The service must be called prior to calling bbos_start which will
 * actually start the system.
 */
void
bbos_init()
{
  /* Basic architecture initialization */
  arch_init();

  /* Initialize target process */
  bbos_process_init();

  /* Initialize scheduler */
  bbos_sched_init();
}
/**
 * bbos_test - Test BBOS settings and components.
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

  bbos_panic("Scheduling has been ended.\n");
}



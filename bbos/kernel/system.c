/*
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

#include <stdio.h>

#include <bbos/kernel/system.h>
#include <bbos/kernel/error_codes.h>
#include <bbos/kernel/idle.h>

/**
 * Halt the system. Display a message, then perfom cleanups with exit.
 *
 * @param fmt The text string to print.
 *
 * @return
 *
 * The function should never return.
 */
void
bbos_panic(const char *fmt, ...)
{
#ifdef BBOS_DEBUG
  static char buf[128];
  va_list args;
  va_start(args, fmt);
  //vsnprintf(buf, sizeof(buf), fmt, args);
  va_end(args);
  printf("Panic: %s\n", buf);
#endif
  //exit(0);
}

#ifdef BBOS_SCHED_ENABLED
#ifndef BBOS_SWITCH_THREAD_HACK
/**
 * Switch to the next thread.
 */
void
bbos_switch_thread()
{
  assert(bbos_sched_myself() < BBOS_NUMBER_OF_THREADS);
  bbos_thread_execute( bbos_sched_myself() );
}
#endif
#endif

/**
 * Start the thread and schedule it.
 *
 * @param tid Thread identifier.
 * @param thread Pointer to the thread.
 *
 * @return
 *
 * Kernel error code.
 */
bbos_error_t 
bbos_start_thread(bbos_thread_id_t tid, void (*thread)(void)) 
{
  assert(tid < BBOS_NUMBER_OF_THREADS);
  bbos_thread_init(tid, thread);
#ifdef BBOS_SCHED_ENABLED
  bbos_sched_enqueue(tid);
#endif
  return BBOS_SUCCESS;
}

/**
 * Stop the thread and dequeue it from schedule.
 *
 * @param tid Thread identifier.
 *
 * @return
 *
 * Kernel error code.
 */
bbos_error_t
bbos_stop_thread(bbos_thread_id_t tid)
{
  assert(tid < BBOS_NUMBER_OF_THREADS);
  bbos_thread_init(tid, NULL);
#ifdef BBOS_SCHED_ENABLED
  bbos_sched_dequeue(tid);
#endif
  return BBOS_SUCCESS;
}

/**
 * The first function that you must call, while will initialize the kernel.
 *
 * @note
 *
 * A requirement of BBOS is that you call bbos_init() before you invoke 
 * any of its other services.
 */
void
bbos_init()
{
  bbos_thread_id_t tid;

#ifdef BBOS_DEBUG
  printf("Initialize BBOS kernel\n");
#endif

  for (tid=0; tid<BBOS_NUMBER_OF_THREADS; tid++)
    bbos_thread_init(tid, NULL);

#ifdef BBOS_SCHED_ENABLED
  bbos_sched_init();
#else
  printf("Scheduler was not enabled\n");
#endif
}

/**
 * Start the kernel.
 */
void
bbos_start()
{
#ifdef BBOS_DEBUG
  printf("Start BBOS kernel\n");
#endif

#ifdef BBOS_SCHED_ENABLED
  bbos_start_thread(BBOS_IDLE, bbos_idle);

  while (1)
    {
      bbos_sched_move();
      bbos_switch_thread();
    }
#else
  bbos_switch_thread();
#endif
}



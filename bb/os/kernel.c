/*
 * Copyright (c) 2012 Sladeware LLC
 */
#include <bb/os/kernel.h>

bbos_thread_t bbos_kernel_threads[BBOS_NR_THREADS];

/* Initialize thread. */
void
bbos_kernel_init_thread(bbos_thread_id_t tid, bbos_thread_runner_t runner,
                        bbos_port_id_t pid)
{
  bbos_validate_thread_id(tid);
  bbos_thread_set_runner(tid, runner);
  bbos_thread_set_port_id(tid, pid);
}

void
bbos_thread_run(bbos_thread_id_t tid)
{
  bbos_validate_thread_id(tid);
  bbos_kernel_assert(bbos_thread_get_runner(tid) != NULL);
  (*bbos_thread_get_runner(tid))();
}

/* Halt the system. Display a message, then perform cleanups with exit. */
void
bbos_kernel_panic(const int8_t* fmt, ...)
{
#ifdef BBOS_DEBUG
  static int8_t buf[128];
  va_list args;
  va_start(args, fmt);
  vsnprintf(buf, sizeof(buf), fmt, args);
  va_end(args);
  printf("Panic: %s\n", buf);
#endif
  exit(0);
}

/**
 * The first function that system calls, while will initialize the
 * kernel.
 *
 * @note
 *
 * A requirement of BBOS is that you call bbos_kenrel_init() before you
 * invoke any of its other services.
 */
void
bbos_kernel_init()
{
  bbos_thread_id_t tid;

  printf("Initialize kernel\n");
  /* Initialize threads */
  for (tid = 0; tid < BBOS_NR_THREADS; tid++)
    {
      bbos_kernel_init_thread(tid, NULL, 0);
    }
  /* Initialize scheduler */
  printf("Initialize scheduler '" BBOS_SCHED_NAME "'\n");
  bbos_sched_init();
  /* ITC */
#ifdef BBOS_KERNEL_ITC
  bbos_kernel_init_itc();
#endif /* BBOS_KERNEL_ITC */
}

/* The main loop can be overload by static scheduler in BBOS_H file. */
#ifndef bbos_kernel_loop
static void
bbos_kernel_loop()
{
  /* Do the main loop */
  while (TRUE)
    {
      bbos_sched_move();
      bbos_kernel_switch_context();
    }
}
#endif

void
bbos_kernel_enable_all_threads()
{
  bbos_thread_id_t tid;
  for (tid = 0; tid < BBOS_NR_THREADS; tid++)
    {
      bbos_kernel_enable_thread(tid);
    }
}

void
bbos_idle_runner()
{
}

/**
 * Start the kernel.
 */
void
bbos_kernel_start()
{
  printf("Start kernel\n");
  bbos_kernel_init_thread(BBOS_IDLE, bbos_idle_runner, 0);
  bbos_kernel_enable_thread(BBOS_IDLE);
  bbos_kernel_loop();
}

void
bbos_kernel_stop()
{
  printf("Stop kernel\n");
  exit(0);
}
/*
 * Copyright (c) 2012 Sladeware LLC
 */
#include <bb/os/kernel.h>

/* Banner */
const static char bbos_banner[] = "BBOS version " BBOS_VERSION_STR  \
  " (" BB_PLATFORM_NAME ")"                                         \
  " (" BB_COMPILER_NAME ")"                                         \
  "\n";

bbos_thread_t bbos_threads[BBOS_NR_THREADS];
bbos_port_t bbos_ports[BBOS_NR_PORTS];

/* Initialize thread. */
void
bbos_thread_init(bbos_thread_id_t tid, bbos_thread_target_t target,
            bbos_port_id_t pid)
{
  bbos_validate_thread_id(tid);
#if BBOS_NR_PORTS > 0
  bbos_validate_port_id(pid);
#endif
  bbos_thread_set_target(tid, target);
  bbos_thread_set_port_id(tid, pid);
}

void
bbos_thread_run(bbos_thread_id_t tid)
{
  bbos_validate_thread_id(tid);
  bbos_assert(bbos_thread_get_target(tid) != NULL);
  (*bbos_thread_get_target(tid))();
}

/* Halt the system. Display a message, then perform cleanups with exit. */
void
bbos_panic(const int8_t* fmt, ...)
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
 * A requirement of BBOS is that you call bbos_init() before you
 * invoke any of its other services.
 */
void
bbos_init()
{
  bbos_thread_id_t tid;

  printf("Initialize kernel\n");
  /* Initialize threads */
  for (tid = 0; tid < BBOS_NR_THREADS; tid++)
    {
      bbos_thread_init(tid, NULL, 0);
    }
  /* Initialize scheduler */
  printf("Initialize scheduler '" BBOS_SCHED_NAME "'\n");
  sched_init();
}

/* The main loop can be overload by static scheduler in BBOS_H file. */
#ifndef bbos_loop
static void
bbos_loop()
{
  /* Do the main loop */
  while (TRUE)
    {
      sched_move();
      bbos_switch_context();
    }
}
#endif

void
bbos_idle_runner()
{
}

/**
 * Start the kernel.
 */
void
bbos_start()
{
  printf("Start kernel\n");

  bbos_thread_init(BBOS_IDLE, bbos_idle_runner, 0);
  bbos_activate_thread(BBOS_IDLE);

  bbos_loop();
}

/**
 * BBOS entry point. It works in several ways. The user may define
 * bbos_main() function to describe application functionally. In this
 * case the system will automatically initialize itself and start the
 * kernel. Otherwise user will have to call bbos_start() manually.
 */
void
bbos()
{
  printf("%s", bbos_banner);
  bbos_init();
#ifdef bbos_main
  bbos_main();
  bbos_start();
#endif
}

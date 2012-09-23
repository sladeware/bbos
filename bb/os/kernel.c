/*
 * This file implements kernel.h interface.
 *
 * Copyright (c) 2012 Sladeware LLC
 * Author: Oleksandr Sviridenko
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *       http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include <bb/os/kernel.h>

void
bbos_kernel_init_thread(bbos_thread_id_t tid, bbos_thread_runner_t runner)
{
  //bbos_validate_thread_id(tid);
  //bbos_thread_set_runner(tid, runner);
}

void
bbos_kernel_init()
{
#if 0
  bbos_thread_id_t tid;
  //bbos_printf("Initialize kernel\n");

  /* Initialize threads. */
  for (tid = 0; tid < BBOS_NUM_THREADS; tid++) {
    bbos_kernel_init_thread(tid, NULL);
  }
#endif

  /* Initialize scheduler. */
#if 0
  //bbos_printf("Initialize scheduler '" BBOS_SCHED_NAME "'\n");
  bbos_sched_init();
#endif
  // Inter-thread communication
#ifdef BBOS_KERNEL_ITC
  bbos_kernel_init_itc();
#endif /* BBOS_KERNEL_ITC */
}

void
bbos_kernel_main()
{
}

#ifndef BBOS_CONFIG_USE_STATIC_SCHED

/* Switches execution context. Start next thread selected by scheduler. */
#define bbos_kernel_switch_context()                                 \
  do {                                                               \
    bbos_validate_thread_id(bbos_sched_identify_myself());           \
    bbos_thread_run(bbos_sched_identify_myself());                   \
  } while (0)

static void
bbos_kernel_loop()
{
  while (TRUE) {
    bbos_sched_move();
    bbos_kernel_switch_context();
    bbos_kernel_main();
  }
}

void
bbos_thread_run(bbos_thread_id_t tid)
{
  bbos_validate_thread_id(tid);
  bbos_kernel_assert(bbos_thread_get_runner(tid) != NULL);
  (*bbos_thread_get_runner(tid))();
}

void
bbos_kernel_enable_all_threads()
{
  bbos_thread_id_t tid;
  for (tid = 0; tid < BBOS_NUM_THREADS; tid++) {
    bbos_kernel_enable_thread(tid);
  }
}

#endif /* BBOS_CONFIG_USE_STATIC_SCHED */

static void bbos_kernel_test()
{
  // Check number of threads
  if (BBOS_NUM_THREADS < 1) {
    //bbos_kernel_panic("System requires atleast one thread\n");
  }
  // By default the number of ports in zero. In this case port interface wont be
  // supported.
  if (BBOS_NUM_THREADS < 0) {
    //bbos_kernel_panic("Number of threads cannot be less than zero\n");
  }
}

// Start the kernel.
void bbos_kernel_start()
{
  //bbos_printf("Start kernel\n");
  bbos_kernel_test();
}

void
bbos_kernel_stop()
{
  //bbos_printf("Stop kernel\n");
  //exit(0);
}

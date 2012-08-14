// Copyright (c) 2012 Sladeware LLC
//
// Author: Oleksandr Sviridenko
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//       http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
// This file implements kernel.h interface.

#include <bb/os/kernel.h>

// Initialize thread.
void bbos_kernel_init_thread(bbos_thread_id_t tid, bbos_thread_runner_t runner)
{
  bbos_validate_thread_id(tid);
  bbos_thread_set_runner(tid, runner);
}

void bbos_thread_run(bbos_thread_id_t tid)
{
  bbos_validate_thread_id(tid);
  bbos_kernel_assert(bbos_thread_get_runner(tid) != NULL);
  (*bbos_thread_get_runner(tid))();
}

// Halt the system. Display a message, then perform cleanups with exit.
void bbos_kernel_panic(const int8_t* fmt, ...)
{
#ifdef BBOS_DEBUG
  static int8_t buf[128];
  va_list args;
  va_start(args, fmt);
  vsnprintf(buf, sizeof(buf), fmt, args);
  va_end(args);
  printf("Panic: %s\n", buf);
#endif
  //exit(0);
}

// The first function that system calls, while will initialize the kernel.
//
// NOTE: A requirement of BBOS is that you call bbos_kenrel_init() before
// you invoke any of its other services.
void bbos_kernel_init()
{
  bbos_thread_id_t tid;

  //bbos_printf("Initialize kernel\n");
  // Initialize threads
  for (tid = 0; tid < BBOS_NR_THREADS; tid++) {
    bbos_kernel_init_thread(tid, NULL);
  }
  // Initialize scheduler
  //bbos_printf("Initialize scheduler '" BBOS_SCHED_NAME "'\n");
  bbos_sched_init();
  // Inter-thread communication
#ifdef BBOS_KERNEL_ITC
  bbos_kernel_init_itc();
#endif // BBOS_KERNEL_ITC
}

static void bbos_kernel_loop()
{
  // Do the main loop
  while (TRUE) {
    bbos_sched_move();
    bbos_kernel_switch_context();
    bbos_kernel_main();
  }
}

void bbos_kernel_main()
{
}

void bbos_kernel_enable_all_threads()
{
  bbos_thread_id_t tid;
  for (tid = 0; tid < BBOS_NR_THREADS; tid++) {
    bbos_kernel_enable_thread(tid);
  }
}

static void bbos_kernel_test()
{
  // Check number of threads
  if (BBOS_NR_THREADS < 1) {
    bbos_kernel_panic("System requires atleast one thread\n");
  }
  // By default the number of ports in zero. In this case port interface wont be
  // supported.
  if (BBOS_NR_THREADS < 0) {
    bbos_kernel_panic("Number of threads cannot be less than zero\n");
  }
}

// Start the kernel.
void bbos_kernel_start()
{
  bbos_printf("Start kernel\n");
  bbos_kernel_test();
  // Finallyze running type and start running
  switch (BBOS_KERNEL_GET_RUNNING_TYPE()) {
  case BBOS_KERNEL_DYNAMIC_RUNNING:
    bbos_kernel_loop();
    break; // we should never be here
  case BBOS_KERNEL_STATIC_RUNNING:
    bbos_kernel_main();
    break;
  }
}

void
bbos_kernel_stop()
{
  //bbos_printf("Stop kernel\n");
  //exit(0);
}

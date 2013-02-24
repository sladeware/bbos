/*
 * BB operating system interface
 *
 * Copyright (c) 2012-2013 Sladeware LLC
 * Author: Oleksand Sviridenko
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
#ifndef __BB_OS_H
#define __BB_OS_H

#include "os/config.h"
#include "os/kernel.h"
#include "os/thread.h"
#include "os/message.h"
#include "os/port.h"
#include BBOS_PROCESSOR_FILE(core.h)

#define BBOS_ITC_ENABLED 0
/* ITC will be provided only if number of ports is greater than zero. */
#if BBOS_NUM_PORTS > 0
#undef BBOS_ITC_ENABLED
#define BBOS_ITC_ENABLED 1
#endif

#if BBOS_ITC_ENABLED
#define BBOS_MESSAGE_SIZE (sizeof(bbos_message_t) + BBOS_MAX_MESSAGE_PAYLOAD_SIZE)

extern bbos_port_t bbos_ports[];
#endif /* BBOS_ITC_ENABLED */

#define BBOS_ASSERT(expr)                       \
  do {                                          \
    if (!(expr)) {                              \
      bbos_assert(__FILE__, __LINE__, #expr);   \
    }                                           \
  } while (0)

extern bbos_thread_id_t bbos_running_threads[BBOS_NUM_KERNELS];

/**
 * Returns ID of the thread that is currently running.
 */
#define bbos_get_running_thread() \
  bbos_running_threads[ bbos_get_core_id() ]

#define bbos_set_running_thread(id) \
  bbos_running_threads[ bbos_get_core_id() ] = (id)

PROTOTYPE(void bbos_assert, (char* filename, int line, char* expr));

PROTOTYPE(void bbos, ());

/**
 * Halt the system. Display a message, then perform cleanups with exit.
 */
PROTOTYPE(void bbos_panic, (const char* fmt, ...));

/*
 * The implementation of the following prototypes has to be generated and
 * presented in os_autogen.c
 */
PROTOTYPE(void bbos_init, ());

#if BBOS_ITC_ENABLED
bbos_message_t* bbos_send_message(bbos_thread_id_t tid);
bbos_message_t* bbos_receive_message();
void bbos_deliver_messages();
#endif /* BBOS_ITC_ENABLED */

#endif /* __BB_OS_H */

/*
 * Copyright (c) 2012 Sladeware LLC
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

#define BBOS_ITC_ENABLED 0
/* ITC will be provided only if number of ports is greater than zero. */
#if BBOS_NR_PORTS > 0
#undef BBOS_ITC_ENABLED
#define BBOS_ITC_ENABLED 1
#endif

#if BBOS_ITC_ENABLED
#define BBOS_MAX_PACKET_SIZE (sizeof(bbos_message_header_t) + BBOS_MAX_MESSAGE_SIZE)

extern bbos_port_t bbos_ports[];

bbos_message_t* bbos_alloc_message(bbos_thread_id_t id);
void bbos_send_message(bbos_message_t* msg);
bbos_message_t* bbos_receive_message();
void bbos_free_message(bbos_message_t* msg);

#endif /* BBOS_ITC_ENABLED > 0 */

#define BBOS_ASSERT(expr)                       \
  do {                                          \
    if (!(expr)) {                              \
      bbos_assert(__FILE__, __LINE__, #expr);   \
    }                                           \
  } while (0)

PROTOTYPE(void bbos_assert, (char* filename, int line, char* expr));

PROTOTYPE(void bbos, ());

/* Halt the system. Display a message, then perform cleanups with exit. */
PROTOTYPE(void bbos_panic, (const int8_t* fmt, ...));

/*
 * The implementation of the following prototypes has to be generated and
 * presented in os_autogen.c
 */
PROTOTYPE(void bbos_init, ());

#endif /* __BB_OS_H */

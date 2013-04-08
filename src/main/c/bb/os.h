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

#define BBOS

#include "bb/os/config.h"
#include "bb/os/kernel.h"
#include "bb/os/thread.h"
#include "bb/os/mm/mempool.h"
#include BBOS_PROCESSOR_FILE(core.h)

/**
 * Message structure passed between threads.
 */
struct bbos_message {
  bbos_port_id_t receiver;
  bbos_port_id_t sender;
  bbos_message_label_t label; /* what kind of message is it */
  void* payload;
};

struct bbos_port {
  mempool pool;
  struct bbos_message** inbox;
  size_t capacity;
  size_t counter; /* count number of unread messages. */
};

/**
 * This array keeps an ID of running thread per kernel/core.
 */
extern bbos_thread_id_t bbos_running_threads[BBOS_NUM_KERNELS];

/******************************************************************************
 * MACROS                                                                     *
 ******************************************************************************/

#define BBOS_ASSERT(expr)                       \
  do {                                          \
    if (!(expr)) {                              \
      bbos_assert(__FILE__, __LINE__, #expr);   \
    }                                           \
  } while (0)

/**
 * Returns ID of the thread that is currently running.
 */
#define bbos_get_running_thread() \
  bbos_running_threads[ bbos_get_core_id() ]

#define bbos_set_running_thread(id) \
  bbos_running_threads[ bbos_get_core_id() ] = (id)

/* ITC will be provided only if number of ports is greater than zero. */
#define BBOS_ITC_ENABLED 0
#if BBOS_NUM_PORTS > 0
#undef BBOS_ITC_ENABLED
#define BBOS_ITC_ENABLED 1
#endif

#define BBOS_MAX_MESSAGE_SIZE                                   \
  (10)
//(sizeof(struct bbos_message) + BBOS_MAX_MESSAGE_PAYLOAD_SIZE)

/**
 * Receives a new message for the running thread. See also
 * bbos_receive_message_from().
 */
#define bbos_receive_message()                                          \
  bbos_receive_message_from((bbos_port_id_t)bbos_get_running_thread())

/******************************************************************************
 * PROTOTYPES                                                                 *
 ******************************************************************************/

PROTOTYPE(void bbos_port_init, (bbos_port_id_t id, size_t capacity,
                                mempool pool, struct bbos_message** inbox));
PROTOTYPE(int8_t bbos_port_is_empty, (bbos_port_id_t id));
PROTOTYPE(int8_t bbos_port_is_full, (bbos_port_id_t id));

PROTOTYPE(struct bbos_message* bbos_request_message, (bbos_port_id_t id));
PROTOTYPE(void bbos_send_message, (struct bbos_message* msg));
PROTOTYPE(struct bbos_message* bbos_receive_message_from, (bbos_port_id_t id));
PROTOTYPE(void bbos_delete_message, (struct bbos_message* msg));

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

#endif /* __BB_OS_H */

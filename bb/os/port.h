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
#ifndef __BB_OS_PORT_H
#define __BB_OS_PORT_H

#include "thread.h"
#include "message.h"
#include "mm/mempool.h"

typedef bbos_thread_id_t bbos_port_id_t;

struct bbos_port {
  mempool_t pool;
  int16_t counter; /* count number of unread messages. */
  int16_t capacity;
  bbos_message_record_t** stack;
};

typedef struct bbos_port bbos_port_t;

/* Macros */

/* NOTE: for internal use only */
#define BBOS_PORT_IS_FULL(pid)                        \
  (bbos_ports[pid].capacity == bbos_ports[pid].counter)

/* Prototypes */

void bbos_port_init(bbos_port_id_t id, size_t capacity, mempool_t pool,
                    bbos_message_record_t** stack);

int8_t bbos_port_is_full(bbos_port_id_t id);

#endif /* __BB_OS_PORT_H */

/*
 * This file implements os.h interface.
 *
 * Copyright (c) 2012-2013 Sladeware LLC
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
 *
 * Author: Oleksandr Sviridenko
 */

#include "bb/os.h"
#include "bb/os/light_stdio.h"
#include BB_STDLIB_FILE(stdlib.h)

// Internal macro to check port id
#define ASSERT_PORT_ID(id) BBOS_ASSERT((id) < BBOS_NUM_PORTS)

#define PORT_IS_EMPTY(id) (bbos_ports[id].counter == 0)
#define PORT_IS_FULL(id) (bbos_ports[id].capacity == bbos_ports[id].counter)

// This array keeps IDs for running threads for each kernel.
bbos_thread_id_t bbos_running_threads[BBOS_NUM_KERNELS];

// Array of ports
struct bbos_port bbos_ports[BBOS_NUM_PORTS];

// BBOS banner!
#ifndef BBOS_CONFIG_SKIP_BANNER_PRINTING
const static char bbos_banner[] = "BBOS version " BBOS_VERSION_STR  \
  " (" BB_HOST_PLATFORM_NAME ")"                                    \
  " (" BB_COMPILER_NAME ")"                                         \
  "\n";
#endif /* BBOS_CONFIG_SKIP_BANNER_PRINTING */

void
bbos_panic(const char* frmt, ...)
{
#if 0
  //#ifdef BBOS_DEBUG
  va_list args;
  bb_printf("PANIC:");
  va_start(args, frmt);
  bb_vprintf(frmt, args);
  va_end(args);
  //#endif
#endif
  exit(0);
}

void
bbos_assert(char* filename, int line, char* expr)
{
  bbos_panic("ASSERT:%s:%d: %s\n", filename, line, expr);
}

void
bbos_port_init(bbos_port_id_t id, size_t capacity, mempool pool,
               struct bbos_message** inbox)
{
  ASSERT_PORT_ID(id);
  // TODO(d2rk): assert null pool
  BBOS_ASSERT(inbox != NULL);
  bbos_ports[id].capacity = capacity;
  bbos_ports[id].counter = 0;
  bbos_ports[id].pool = pool;
  bbos_ports[id].inbox = inbox;
}

int8_t
bbos_port_is_empty(bbos_port_id_t id)
{
  ASSERT_PORT_ID(id);
  return PORT_IS_EMPTY(id);
}

int8_t
bbos_port_is_full(bbos_port_id_t id)
{
  ASSERT_PORT_ID(id);
  return PORT_IS_FULL(id);
}

struct bbos_message*
bbos_request_message(bbos_port_id_t id)
{
  struct bbos_message* msg;
  ASSERT_PORT_ID(id);
  if ((msg = (struct bbos_message*)mempool_alloc(&bbos_ports[id].pool)) == NULL) {
    return NULL;
  }
  msg->receiver = id;
  msg->sender = bbos_get_running_thread();
  msg->label = 0; /* NO_LABEL? */
  msg->payload = (void*)((void*)msg + sizeof(struct bbos_message));
  return msg;
}

void
bbos_send_message(struct bbos_message* msg)
{
  BBOS_ASSERT(msg != NULL);
  ASSERT_PORT_ID(msg->receiver); /* redundant? */
  //*(++bbos_ports[msg->receiver].inbox) = msg;
  *bbos_ports[msg->receiver].inbox = msg;
  bbos_ports[msg->receiver].inbox++;
  bbos_ports[msg->receiver].counter++;
}

struct bbos_message*
bbos_receive_message_from(bbos_port_id_t id)
{
  struct bbos_message* msg;
  if (PORT_IS_EMPTY(id)) {
    return NULL;
  }
  //msg = *(--bbos_ports[id].inbox);
  bbos_ports[id].inbox--;
  msg = *bbos_ports[id].inbox;
  bbos_ports[id].counter--;
  return msg;
}

void
bbos_delete_message(struct bbos_message* msg)
{
  BBOS_ASSERT(msg != NULL);
  mempool_free(&bbos_ports[msg->receiver].pool, msg);
}

void
bbos()
{
#ifndef BBOS_CONFIG_SKIP_BANNER_PRINTING
  //printf("%s", bbos_banner);
#endif /* BBOS_CONFIG_SKIP_BANNER_PRINTING */
  bbos_init();
}

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

//#define PRINT_DEBUG(frmt, args...) sio_cogsafe_printf(frmt, args)
#define PRINT_DEBUG(frmt, args...) do {} while (0)

HUBDATA int messaging_lock = 0;

/* Internal macro to check port id. */
#define ASSERT_PORT_ID(id) BBOS_ASSERT((id) < BBOS_NUM_PORTS)

#define PORT_IS_EMPTY(id) (bbos_ports[id].head == bbos_ports[id].tail)

#define PORT_IS_FULL(id) \
  (((bbos_ports[id].tail + 1) % (bbos_ports[id].capacity)) == bbos_ports[id].head)

// We need this only in case of multicore support
#define LOCK_PORT(id)                           \
  do {                                          \
    while (!lockset(messaging_lock));           \
  } while (0)

#define UNLOCK_PORT(id)                         \
  do {                                          \
    lockclr(messaging_lock);                    \
  } while (0)

/* This array keeps IDs for running threads for each kernel. */
HUBDATA bbos_thread_id_t bbos_running_threads[BBOS_NUM_KERNELS];

/* Array of available ports for thread communication purposes. */
HUBDATA struct bbos_port bbos_ports[BBOS_NUM_PORTS];

/* BBOS banner! */
#ifndef BBOS_CONFIG_SKIP_BANNER_PRINTING
HUBDATA const static char bbos_banner[] = "BBOS version " BBOS_VERSION_STR \
  " (" BB_HOST_PLATFORM_NAME ")"                                        \
  " (" BB_COMPILER_NAME ")"                                             \
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
  exit(0);
#endif
}

void
bbos_assert(char* filename, int line, char* expr)
{
  bbos_panic("ASSERT:%s:%d: %s\n", filename, line, expr);
}

void
bbos_port_init(bbos_port_id_t id, size_t capacity, const int8_t* part,
               struct bbos_message** inbox)
{
  ASSERT_PORT_ID(id);
  // TODO(d2rk): assert null pool
  BBOS_ASSERT(inbox != NULL);
  BBOS_ASSERT(part != NULL);
  PRINT_DEBUG("[I] Init port %d[capacity=%d, part=0x%x, inbox=0x%x]\n",
              id, capacity, part, inbox);
  bbos_ports[id].capacity = capacity;
  bbos_ports[id].pool = mempool_init(part, capacity, BBOS_MAX_MESSAGE_SIZE);;
  bbos_ports[id].head = bbos_ports[id].tail = 0;
  bbos_ports[id].inbox = inbox;
  bbos_ports[id].lock = 0;
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
  LOCK_PORT(id);
  PRINT_DEBUG("[I] Thread %d requests message from port %d\n",
              bbos_get_running_thread(), id);
  if ((msg = (struct bbos_message*)mempool_alloc(bbos_ports[id].pool)) == NULL) {
    PRINT_DEBUG("[I] Port %d doesn't have free messages\n", id);
    return NULL;
  }
  UNLOCK_PORT(id);
  msg->receiver = id;
  msg->sender = bbos_get_running_thread();
  msg->label = 0; /* BBOS_NOT_LABELED_MESSAGE ? */
  msg->payload = (void*)((void*)msg + sizeof(struct bbos_message));
  return msg;
}

void
bbos_send_message(struct bbos_message* msg)
{
  bbos_port_id_t id;
  BBOS_ASSERT(msg != NULL);
  id = msg->receiver;
  ASSERT_PORT_ID(id); /* redundant? */
  LOCK_PORT(id);
  if (PORT_IS_FULL(id)) {
    /*
     * This should never happen unless the message receiver was manually
     * changed.
     */
    return;
  }
  PRINT_DEBUG("[I] Thread %d sends message 0x%x with label %d to %d\n",
              msg->sender, msg, msg->label, msg->receiver);
  bbos_ports[id].inbox[bbos_ports[id].tail] = msg;
  bbos_ports[id].tail = (bbos_ports[id].tail + 1) % (bbos_ports[id].capacity);
  UNLOCK_PORT(id);
}

struct bbos_message*
bbos_receive_message_from(bbos_port_id_t id)
{
  struct bbos_message* msg;
  if (PORT_IS_EMPTY(id)) {
    return NULL;
  }
  LOCK_PORT(id);
  msg = bbos_ports[id].inbox[bbos_ports[id].head];
  bbos_ports[id].head = (bbos_ports[id].head + 1) % (bbos_ports[id].capacity);
  PRINT_DEBUG("[I] Thread %d receives a message 0x%x with label %d from %d\n",
              id, msg, msg->label, msg->sender);
  UNLOCK_PORT(id);
  return msg;
}

void
bbos_delete_message(struct bbos_message* msg)
{
  bbos_port_id_t id;
  BBOS_ASSERT(msg != NULL);
  id = msg->receiver;
  LOCK_PORT(id);
  PRINT_DEBUG("[I] Thread %d deletes message 0x%x from %d\n",
              bbos_get_running_thread(), msg, id);
  mempool_free(bbos_ports[id].pool, msg);
  UNLOCK_PORT(id);
}

void
bbos()
{
#ifndef BBOS_CONFIG_SKIP_BANNER_PRINTING
  //printf("%s", bbos_banner);
#endif /* BBOS_CONFIG_SKIP_BANNER_PRINTING */
  messaging_lock = locknew();
  bb_sio_init();
  bbos_init();
}

/*
 * This file implements os.h interface.
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

#include <bb/os.h>
#include <bb/os/light_stdio.h>
#include BB_STDLIB_FILE(stdlib.h)

#ifndef BBOS_CONFIG_SKIP_BANNER_PRINTING
const static char bbos_banner[] = "BBOS version " BBOS_VERSION_STR  \
  " (" BB_HOST_PLATFORM_NAME ")"                                    \
  " (" BB_COMPILER_NAME ")"                                         \
  "\n";
#endif /* BBOS_CONFIG_SKIP_BANNER_PRINTING */

#if BBOS_ITC_ENABLED

bbos_message_t*
bbos_alloc_message(bbos_thread_id_t id)
{
  bbos_message_record_t* record;
  BBOS_ASSERT(id < BBOS_NR_PORTS);
  if (BBOS_PORT_IS_FULL(id)) {
    return NULL;
  }
  record = (bbos_message_record_t*)mempool_alloc(bbos_ports[id].pool);
  /* Just for testing; if port is not full, we always have memory. */
  BBOS_ASSERT(record != NULL);
  record->owner = id;
  record->message.payload = &record->message.payload + 1;
  return &record->message;
}

void
bbos_send_message(bbos_message_t* msg)
{
  //BBOS_ASSERT(id < BBOS_NR_PORTS);
  //bbos_ports[id].stack[ bbos_ports[id].counter ] = BBOS_GET_MESSAGE_PACKET(msg);
  //bbos_ports[id].counter++;
}

bbos_message_t*
bbos_receive_message()
{
  //bbos_ports[id].counter--;
  //return bbos_ports[id].stack[ bbos_ports[id].counter ];
  return NULL;
}

void
bbos_free_message(bbos_message_t* msg)
{
  //BBOS_ASSERT(id < BBOS_NR_PORTS);
  //mempool_free(bbos_ports[id].pool, BBOS_GET_MESSAGE_PACKET(msg));
}

#endif /* BBOS_ITC_ENABLED */

void
bbos_panic(const int8_t* frmt, ...)
{
  //#ifdef BBOS_DEBUG
  va_list args;
  bb_printf("PANIC:");
  va_start(args, frmt);
  bb_vprintf(frmt, args);
  va_end(args);
  //#endif
  exit(0);
}

void
bbos_assert(char* filename, int line, char* expr)
{
  bb_printf("ASSERT:%s:%d: %s", filename, line, expr);
  bbos_panic("assertation failed.");
}

void
bbos()
{
#ifndef BBOS_CONFIG_SKIP_BANNER_PRINTING
  bb_printf("%s", bbos_banner);
#endif /* BBOS_CONFIG_SKIP_BANNER_PRINTING */
  bbos_init();
}

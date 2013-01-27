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

bbos_thread_id_t bbos_running_threads[BBOS_NUM_KERNELS];

#ifndef BBOS_CONFIG_SKIP_BANNER_PRINTING
const static char bbos_banner[] = "BBOS version " BBOS_VERSION_STR  \
  " (" BB_HOST_PLATFORM_NAME ")"                                    \
  " (" BB_COMPILER_NAME ")"                                         \
  "\n";
#endif /* BBOS_CONFIG_SKIP_BANNER_PRINTING */

#if BBOS_ITC_ENABLED

bbos_message_t*
bbos_send_message(bbos_thread_id_t tid)
{
  bbos_message_t* msg;
  BBOS_ASSERT_THREAD_ID(tid);
  if (BBOS_PORT_IS_FULL(tid)) {
    return NULL;
  }
  msg = (bbos_message_t*)mempool_alloc(bbos_ports[tid].pool);
  /* Store message as pending and the end of the port's stack. */
  *(--bbos_ports[tid].pending_cursor) = msg;
  return msg;
}

bbos_message_t*
bbos_receive_message()
{
  bbos_thread_id_t tid;
  bbos_message_t msg;
  tid = bbos_get_running_thread();
  if (BBOS_PORT_IS_EMPTY(tid)) {
    return NULL;
  }
  return *(++bbos_ports[tid].garbage_cursor);
}

void
bbos_deliver_messages()
{
}

#endif /* BBOS_ITC_ENABLED */

void
bbos_panic(const char* frmt, ...)
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

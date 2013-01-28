/*
 * This file implements port.h interface.
 *
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
#include <bb/os.h>

void
bbos_port_init(bbos_port_id_t id, size_t capacity, mempool_t pool,
	       bbos_message_t** stack)
{
  BBOS_ASSERT(id < BBOS_NUM_PORTS);
  bbos_ports[id].capacity = capacity;
  bbos_ports[id].counter = 0;
  bbos_ports[id].pool = pool;
  bbos_ports[id].garbage_cursor = stack;
  bbos_ports[id].pending_cursor = stack + (capacity - 1);
}

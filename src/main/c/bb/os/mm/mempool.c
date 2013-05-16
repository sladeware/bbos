/*
 * This file implements mempool.h interface.
 *
 * Copyright (c) 2012-2013 Sladeware LLC
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

#include "bb/os.h"
#include "bb/os/mm/mempool.h"
#include "bb/os/light_stdio.h"

void
mempool_resize(mempool p, uint16_t n, uint16_t sz)
{
  uint16_t i;
  BBOS_ASSERT(p != NULL);
  for (i = 0; i < n; i++) {
    /*
     * NOTE: Catalina compiler doesn't allow you to do pointer arithmetic with
     * void. We need to cast it first. I think 4 bytes will be enought for most
     * of compilers.
     */
    *(void**)((uint32_t)p + i * sz) = (void*)((uint32_t)p + (i + 1) * sz);
  }
  *(void **)((uint32_t)p + i * sz) = NULL;
}

mempool
mempool_init(const int8_t* p, uint16_t n, uint16_t sz)
{
  BBOS_ASSERT(p != NULL);
  mempool_resize((void*)p, n, sz);
  return (void*)p;
}

void*
mempool_alloc(mempool* p)
{
  void** b;
  BBOS_ASSERT(p != NULL);
  MEMPOOL_ALLOC(p, b);
  return (void *)b;
}

void
mempool_free(mempool* p, void* b)
{
  BBOS_ASSERT(p != NULL);
  BBOS_ASSERT(b != NULL);
  MEMPOOL_FREE(p, b);
}

/*
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

#include "shmem.h"

#include <string.h>

int8_t
shmem_read_byte(int32_t addr)
{
  return *(int8_t*)addr;
}

void
shmem_write_byte(int32_t addr, int8_t byte)
{
  *(int8_t*)addr = byte;
}

/* TODO: More than one long required a lock. */
void
shmem_read(int32_t src_addr, void* dst, size_t n)
{
  memcpy(dst, (void*)src_addr, n);
}

/* TODO: More than one long required a lock. */
void
shmem_write(int32_t dst_addr, void* src, size_t n)
{
  memcpy((void*)dst_addr, src, n);
}

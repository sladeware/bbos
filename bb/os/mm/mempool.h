/*
 * Memory pool allocator or mempool is fast memory allocator with constant time
 * access to dynamic allocation for fixed-size chunks of memory. No footprint,
 * just one void pointer to keep the pool.
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
#ifndef __BB_OS_MM_MEMPOOL_H
#define __BB_OS_MM_MEMPOOL_H

#include <bb/os/config.h>
#include BB_STDLIB_FILE(stddef.h)

typedef void* mempool_t;

/**
 * Create new memory partition name with size n * sz bytes.
 */
#define MEMPOOL_PARTITION(name, n, sz)          \
  int8_t name[n * sz]

/**
 * Just an alias for MEMPOOL_PARTITION.
 */
#define MEMPOOL_PART MEMPOOL_PARTITION

/**
 * Allocate a block of memory from the pool. Basically used for better
 * performance.
 */
#define MEMPOOL_ALLOC(pool, block)              \
  do {                                          \
    if ((block = (void**)*pool) != NULL) {      \
      *pool = *block;                           \
    }                                           \
  } while (0)

/**
 * Free a memory block.
 */
#define MEMPOOL_FREE(pool, block)               \
  do {                                          \
    if (block != NULL) {                        \
      *((void**)block) = *pool;                 \
      *pool = (void*)block;                     \
    }                                           \
  } while (0)

/* Prototypes */

/**
 * Initializes memory pool. Returns pointer to the first free memory block.
 *
 * NOTE: as close block size sz or number of blocks n to the power of 2, as
 * faster.
 *
 * It is the application's responsibility to manage the memory area associated
 * with the pool, which is available after this service completes. In addition,
 * the application must prevent use of a deleted pool or memory previously
 * allocated from it.
 */
PROTOTYPE(mempool_t mempool_init, (const int8_t* p, uint16_t n, uint16_t sz));

/**
 * Resizes an existed memory pool.
 */
PROTOTYPE(void mempool_resize, (mempool_t p, uint16_t n, uint16_t sz));

/**
 * Allocates next free memory block from the memory pool.
 */
PROTOTYPE(void* mempool_alloc, (mempool_t* p));

/**
 * Returns memory block to a memory pool.
 */
PROTOTYPE(void mempool_free, (mempool_t* p, void* b));

#endif /* __BB_OS_MM_MEMPOOL_H */

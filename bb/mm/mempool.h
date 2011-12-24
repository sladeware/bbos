/*
 * Memory pool allocator
 *
 * Copyright (c) 2011 Sladeware LLC
 */

/*
 * mempool is fast memory allocator with constant time access to dynamic
 * allocation for fixed-size chunks of memory.
 *
 * No footprint, just one void pointer to keep the pool.
 */

#ifndef __BB_MM_MEMPOOL_H
#define __BB_MM_MEMPOOL_H

#include <bb/config.h>
#include <bb/stdint.h>

/* Create new memory partition name with size n * sz bytes. */
#define MEMPOOL(name, n, sz)               \
  int8_t name[n * sz]

/*
 * Allocate a block of memory from the pool. Basically used for better
 * performance.
 */
#define MEMPOOL_ALLOC(pool, block)              \
  do                                            \
    {                                           \
      if ((block = (void**)*pool) != NULL)      \
        {                                       \
          *pool = *block;                       \
        }                                       \
    } while (0)

/* Free a memory block. */
#define MEMPOOL_FREE(pool, block)               \
  do                                            \
    {                                           \
      if (block != NULL)                        \
        {                                       \
          *((void**)block) = *pool;             \
          *pool = (void*)block;                 \
        }                                       \
    } while (0)

/* Prototypes */

PROTOTYPE(void* mempool_init, (const void* p, uint16_t n, uint16_t sz));
PROTOTYPE(void  mempool_resize, (const void* p, uint16_t n, uint16_t sz));
PROTOTYPE(void* mempool_alloc, (void** p));
PROTOTYPE(void  mempool_free, (void** p, void* b));

#endif /* __BB_MM_MEMPOOL_H */

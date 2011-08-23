/*
 * Copyright (c) 2011 Sladeware LLC
 */

#ifndef __MM_MEMPOOL_H
#define __MM_MEMPOOL_H

/**
 * @file bb/os/mm/mempool.h
 * @brief Memory pool allocator
 *
 * Memory pool is a memory allocator with constant time access to dynamic
 * allocation for fixed-size chunks of memory.
 *
 * No footprint, just one void pointer to keep the pool.
 */

#include <bbos/kernel/types.h>

/**
 * @def BBOS_MEMPOOL_ALLOC(pool, block)
 * @brief Allocate a block of memory from the pool.
 * @param pool Pointer to the used memory pool
 * @param block Pointer to the memory block
 */
#define BBOS_MEMPOOL_ALLOC(pool, block)         \
  do {                                          \
    if ((block = (void**)*pool) != NULL) {      \
      *pool = *block;                           \
    }                                           \
  } while (0)

/**

 * @def BBOS_MEMPOOL_FREE(pool, block)
 * @brief Free a memory block.
 * @param pool Pointer to the used memory pool
 * @param block Pointer to the memory block
 */
#define BBOS_MEMPOOL_FREE(pool, block)          \
  do {                                          \
    if (block != NULL) {                        \
      *((void**)block) = *pool;                 \
      *pool = (void*)block;                     \
    }                                           \
  } while (0)

/* Prototypes */

PROTOTYPE(void* bbos_mempool_init, (const void* part, uint16 n, uint16 sz));
PROTOTYPE(void bbos_mempool_resize, (const void* part, uint16 n, uint16 sz));
PROTOTYPE(void* bbos_mempool_alloc, (void** pool));
PROTOTYPE(void bbos_mempool_free, (void** pool, void* block));

#endif /* __MM_MEMPOOL_H */

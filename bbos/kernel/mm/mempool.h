/*
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

#ifndef __MEMPOOL_H
#define __MEMPOOL_H

/**
 * @file mempool.h
 * @brief Memory pool allocator
 *
 * Memory pool is a memory allocator with constant time access to dynamic
 * allocation for fixed-size chunks of memory.
 *
 * No footprint, just one void pointer to keep the pool.
 */

#include <bbos/kernel/types.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * Allocate a block of memory from the pool.
 *
 * @param pool Pointer to the used memory pool
 * @param block Pointer to the memory block
 */
#define BBOS_MEMPOOL_ALLOC(pool, block)			\
  do {							\
    if ((block = (void **)*pool) != NULL) {		\
      *pool = *block;					\
    }							\
  } while (0)

/**
 * Free a memory block.
 * 
 * @param pool Pointer to the used memory pool
 * @param block Pointer to the memory block
 */
#define BBOS_MEMPOOL_FREE(pool, block)			\
  do {							\
    if (block != NULL) {				\
      *((void **)block) = *pool;			\
      *pool = (void *)block;				\
    }							\
  } while (0)

/* Prototypes */

void *bbos_mempool_init(const void *part, uint16 n, uint16 sz);
void bbos_mempool_resize(const void *part, uint16 n, uint16 sz);
void *bbos_mempool_alloc(void **pool);
void bbos_mempool_free(void **pool, void *block);

#ifdef __cplusplus
}
#endif

#endif /* __MEMPOOL_H */


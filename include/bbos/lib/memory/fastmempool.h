/*
 * The BBOS memory pool.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_LIB_MEMPOOL_H
#define __BBOS_LIB_MEMPOOL_H

#include <stddef.h>
#include <bbos/env.h>

/** The memory block structure */
struct fastmempool_block {
  /* Next free memory block */
  struct fastmempool_block *next;
};

typedef struct fastmempool_block fastmempool_block_t;

/* The memory pool structure */
struct fastmempool {
  /* Points to the next free memory block */
  fastmempool_block_t *next_free_block;
};

typedef struct fastmempool fastmempool_t;

enum {
  /* The number of bytes used to hold memory pool structure */
  FASTMEMPOOL_OVERHEAD = ((int16_t)sizeof(fastmempool_t))
};

/**
 * Computes size of the memory partition by using specified number
 * of blocks and block size.
 */
#define FASTMEMPOOL_PARTITION_SIZE(num_blocks, block_size) \
  (FASTMEMPOOL_OVERHEAD + num_blocks * block_size)

/**
 * FASTMEMPOOL_PARTITION - Creates memory partition.
 */
#define FASTMEMPOOL_PARTITION(name, num_blocks, block_size) \
  int8_t name[FASTMEMPOOL_PARTITION_SIZE(num_blocks, block_size)]

/* Prototypes */

fastmempool_t *fastmempool_init(const void *part, uint16_t num_blocks, \
				  uint16_t block_size);

void fastmempool_resize(fastmempool_t *pool, uint16_t num_blocks,\
			 uint16_t block_size);

void *fastmempool_alloc(fastmempool_t *pool);

void fastmempool_free(fastmempool_t *pool, void *addr);

#endif /* __BBOS_LIB_MEMPOOL_H */



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
struct bbos_mempool_block {
  /* Next free memory block */
  struct bbos_mempool_block *next;
};

typedef struct bbos_mempool_block bbos_mempool_block_t;

/* The memory pool structure */
struct bbos_mempool {
  /* Points to the next free memory block */
  bbos_mempool_block_t *next_free_block;
};

typedef struct bbos_mempool bbos_mempool_t;

enum {
  /* The number of bytes used to hold memory pool structure */
  BBOS_MEMPOOL_OVERHEAD = ((int16_t)sizeof(bbos_mempool_t))
};

/**
 * Computes size of the memory partition by using specified number
 * of blocks and block size.
 */
#define BBOS_MEMPOOL_PARTITION_SIZE(num_blocks, block_size) \
  (BBOS_MEMPOOL_OVERHEAD + num_blocks * block_size)

/**
 * BBOS_MEMPOOL - Creates memory partition.
 */
#define BBOS_MEMPOOL(name, num_blocks, block_size) \
  int8_t name[BBOS_MEMPOOL_PARTITION_SIZE(num_blocks, block_size)]

/* Prototypes */

bbos_mempool_t *bbos_mempool_init(const void *part, uint16_t num_blocks, \
				  uint16_t block_size);

void bbos_mempool_resize(bbos_mempool_t *pool, uint16_t num_blocks,\
			 uint16_t block_size);

void *bbos_mempool_alloc(bbos_mempool_t *pool);

void bbos_mempool_free(bbos_mempool_t *pool, void *addr);

#endif /* __BBOS_LIB_MEMPOOL_H */



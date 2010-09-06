/*
 * Memory pool.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */
#ifndef __BBOS_MM_MEMPOOL_H
#define __BBOS_MM_MEMPOOL_H

#ifdef __cplusplus
extern "C" {
#endif

/**
 * struct bbos_mempool_block - The memory block structure.
 * @next: Pointer to the next free memory block.
 */
struct bbos_mempool_block {
  /* Next free memory block */
  struct bbos_mempool_block *next;
};

typedef struct bbos_mempool_block bbos_mempool_block_t;

/**
 * struct bbos_mempool - The memory pool structure.
 * @next_free_block: Pointer to the next free memory block.
 *
 * XXX:
 *
 * If we will not provide more fields to the memory pool structure, then
 * make it as a simple variable.
 */
struct bbos_mempool {
  /* Points to the next free memory block */
  struct bbos_mempool_block *next_free_block;
};

typedef struct bbos_mempool bbos_mempool_t;

enum {
  /* The number of bytes used to hold memory pool structure */
  BBOS_MEMPOOL_OVERHEAD = ((int16_t)sizeof(bbos_mempool_t))
};

/*
 * Computes size of the memory partition by using specified number
 * of blocks and block size.
 */
#define BBOS_MEMPOOL_PARTITION_SIZE(num_blocks, block_size) \
  (BBOS_MEMPOOL_OVERHEAD + num_blocks * block_size)

/*
 * Creates memory partition with the specified name.
 */
#define BBOS_MEMPOOL_PARTITION(name, num_blocks, block_size)		\
  int8_t name[BBOS_MEMPOOL_PARTITION_SIZE(num_blocks, block_size)]

/* Prototypes */

struct bbos_mempool *bbos_mempool_create(const void *part, uint16_t num_blocks,\
	uint16_t block_sz);

void bbos_mempool_resize(struct bbos_mempool *pool, uint16_t num_blocks,	\
	uint16_t block_sz);

void *bbos_mempool_alloc(struct bbos_mempool *pool);

void bbos_mempool_free(struct bbos_mempool *pool, void *block);

void bbos_mempool_destroy(struct bbos_mempool *pool);

#ifdef __cplusplus
}
#endif

#endif /* __BBOS_MM_MEMPOOL_H */


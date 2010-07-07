/*
 * Fast memory pool is a memory allocator with constant time access to dynamic 
 * allocation for fixed-size blocks of memory.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 *
 */

#include <bbos/lib/memory/fastmempool.h>

/**
 * fastmempool_init - Initialize memory partition and returns memory pool.
 * @part: Pointer to the memory partition.
 * @n_blocks: Number of blocks in partition.
 * @block_sz: Block size in bytes.
 *
 * Return value:
 *
 * Pointer to the memory pool.
 *
 * Note:
 *
 * The partition should	have the correct size stored in the memory pool 
 * structure (see FASTMEMPOOL_PARTITION_SIZE).
 *
 * As close block size or number of blocks to the power of 2, as faster.
 *
 * Complexity:
 *
 * O(n_blocks), where n_blocks is the number of blocks in partition.
 */
fastmempool_t *
fastmempool_init(const void *part, uint16_t n_blocks, uint16_t block_sz)
{
  fastmempool_t *pool;

  /* Initialize pool */
  pool = (fastmempool_t *)part;
  pool->next_free_block = (fastmempool_block_t *)((int8_t *)part + \
		FASTMEMPOOL_OVERHEAD);

  /* Initialize/Format memory partition */
  fastmempool_resize(pool, n_blocks, block_sz);

  return pool;
}

/**
 * fastmempool_resize - Resizes an existed memory pool. 
 * @pool: Pointer to the used memory pool.
 * @n_blocks: Number of blocks in partition.
 * @block_sz: Block size in bytes.
 *
 * Return value:
 *
 * Pointer to the memory pool.
 *
 * O(n_blocks), where n_blocks is the number of blocks in partition.
 */
void
fastmempool_resize(fastmempool_t *pool, uint16_t n_blocks, uint16_t block_sz)
{
  uint16_t block_id;
  int8_t *start_addr;
  fastmempool_block_t *block;
  fastmempool_block_t *prev_block;

  start_addr = (int8_t *)pool + FASTMEMPOOL_OVERHEAD;
  prev_block=(fastmempool_block_t *)start_addr;
  prev_block->next = NULL;

  /* Initialize memory partition */
  for(block_id=1; block_id < n_blocks; block_id++) {
    block = (fastmempool_block_t *)(start_addr + (block_id * block_sz));
    block->next = NULL;
    prev_block->next = block;
    prev_block = block;
  }
}

/**
 * fastmempool_alloc - Allocates next free memory block from the memory pool.
 * @pool: Pointer to the target memory pool.
 *
 * Return value:
 *
 * Pointer to the memory block or NULL if there are no free blocks.
 *
 * Complexity:
 *
 * O(1)
 */
void *
fastmempool_alloc(fastmempool_t *pool)
{
  fastmempool_block_t *block;

  /* Get next free memory block and move to the next one if possible */
  if ((block = pool->next_free_block) != NULL) {
    pool->next_free_block = block->next;
  }

  /* Return pointer to the next free memory block */
  return (void *)block;
}

/**
 * fastmempool_free - Returns memory block to a memory pool.
 * @pool: Pointer to the used memory pool.
 * @addr: Pointer to the block.
 *
 * Complexity:
 *
 * O(1)
 */
void
fastmempool_free(fastmempool_t *pool, void *addr)
{
  fastmempool_block_t *block;

  /* Don't attempt to free a NULL pointer */
  if (addr == NULL) {
    return;
  }

  block = (fastmempool_block_t *)addr;

  /* Connect block with the chain of free blocks */
  block->next = pool->next_free_block;
  pool->next_free_block = block;
}


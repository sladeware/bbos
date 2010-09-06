/*
 * Memory pool is a memory allocator with constant time access to dynamic
 * allocation for fixed-size blocks of memory.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#include <bbos.h>

/**
 * bbos_mempool_create - Create and return memory pool.
 * @part: Pointer to the memory partition.
 * @n_blocks: Number of blocks in partition.
 * @block_sz: Number of bytes in each memory block.
 *
 * Return value:
 *
 * Pointer to the memory pool.
 *
 * Note:
 *
 * The partition should	have the correct size stored in the memory pool
 * structure (see BBOS_MEMPOOL_PARTITION_SIZE).
 *
 * As close block size or number of blocks to the power of 2, as faster.
 *
 * Description:
 *
 * This service creates a memory pool in the area specified.
 *
 * Complexity:
 *
 * O(n_blocks), where n_blocks is the number of blocks in partition.
 */
struct bbos_mempool *
bbos_mempool_create(const void *part, uint16_t n_blocks, uint16_t block_sz)
{
  bbos_mempool_t *pool;

  /* Initialize pool */
  pool = (bbos_mempool_t *)part;
  pool->next_free_block = (bbos_mempool_block_t *)((int8_t *)part +	\
						   BBOS_MEMPOOL_OVERHEAD);

  /* Initialize/Format memory partition */
  bbos_mempool_resize(pool, n_blocks, block_sz);

  return pool;
}

/**
 * bbos_mempool_resize - Resizes an existed memory pool.
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
bbos_mempool_resize(bbos_mempool_t *pool, uint16_t n_blocks, uint16_t block_sz)
{
  uint16_t block_id;
  int8_t *start_addr;
  bbos_mempool_block_t *block;
  bbos_mempool_block_t *prev_block;

  start_addr = (int8_t *)pool + BBOS_MEMPOOL_OVERHEAD;
  prev_block=(bbos_mempool_block_t *)start_addr;
  prev_block->next = NULL;

  /* Initialize memory partition */
  for(block_id=1; block_id < n_blocks; block_id++) {
    block = (bbos_mempool_block_t *)(start_addr + (block_id * block_sz));
    block->next = NULL;
    prev_block->next = block;
    prev_block = block;
  }
}

/**
 * bbos_mempool_alloc - Allocates next free memory block from the memory
 * pool.
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
bbos_mempool_alloc(bbos_mempool_t *pool)
{
  bbos_mempool_block_t *block;

	assert(pool); // check for NULL pointer

  /* Get next free memory block and move to the next one if possible */
  if ((block = pool->next_free_block) != NULL) {
    pool->next_free_block = block->next;
  }

  /* Return pointer to the next free memory block */
  return (void *)block;
}

/**
 * bbos_mempool_free - Returns memory block to a memory pool.
 * @pool: Pointer to the used memory pool.
 * @addr: Pointer to the block.
 *
 * Complexity:
 *
 * O(1)
 */
void
bbos_mempool_free(bbos_mempool_t *pool, void *addr)
{
  bbos_mempool_block_t *block;

	assert(pool); // check for NULL pointer

  /* Don't attempt to free a NULL pointer */
  if (addr == NULL) {
    return;
  }

  block = (bbos_mempool_block_t *)addr;

  /* Connect block with the chain of free blocks */
  block->next = pool->next_free_block;
  pool->next_free_block = block;
}


/**
 * bbos_mempool_destroy - Destroy memory pool.
 * @pool: Pointer to the memory pool.
 *
 * Note:
 *
 * It is the application’s responsibility to manage the memory area
 * associated with the pool, which is available after this service completes.
 * In addition, the application must prevent use of a deleted pool or memory
 * previously allocated from it.
 */
void
bbos_mempool_destroy(struct bbos_mempool *pool)
{
}




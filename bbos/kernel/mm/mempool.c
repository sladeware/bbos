/*
 * Memory pool is a memory allocator with constant time access to dynamic
 * allocation for fixed-size blocks of memory.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#include <bbos.h>

#if BBOS_NUMBER_OF_MEMPOOLS > 0

struct bbos_mempool bbos_mempool_table[BBOS_NUMBER_OF_MEMPOOLS];

/**
 * bbos_mempool_init - Initialize memory pool.
 * @id: Memory pool identifier.
 * @part: Pointer to the memory partition.
 * @n_blocks: Number of blocks in partition.
 * @block_sz: Number of bytes in each memory block.
 *
 * Return value:
 *
 * Generic error code.
 *
 * Note:
 *
 * As close block size or number of blocks to the power of 2, as faster.
 *
 * It is the application’s responsibility to manage the memory area
 * associated with the pool, which is available after this service completes.
 * In addition, the application must prevent use of a deleted pool or memory
 * previously allocated from it.
 *
 * Complexity:
 *
 * O(n_blocks), where n_blocks is the number of blocks in partition.
 */
bbos_return_t
bbos_mempool_init(bbos_mempool_id_t id, const void *part, uint16_t n, 
  uint16_t sz)
{
  /* Initialize pool */
  bbos_mempool_table[id].next_free_block = (bbos_mempool_block_t *)part;

  /* Initialize/Format memory partition */
  bbos_mempool_resize(id, part, n, sz);

  return BBOS_SUCCESS;
}

/**
 * bbos_mempool_resize - Resize an existed memory pool.
 * @pool: Pointer to the memory pool.
 * @part: Pointer to the used memory pool.
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
bbos_mempool_resize(bbos_mempool_id_t id, const void *part, uint16_t n_blocks, 
  uint16_t block_sz)
{
  uint16_t block_id;
  bbos_mempool_block_t *block;
  bbos_mempool_block_t *prev_block;

  prev_block=(bbos_mempool_block_t *)part;
  prev_block->next = NULL;

  /* Initialize memory partition */
  for(block_id=1; block_id < n_blocks; block_id++) {
    block = (bbos_mempool_block_t *)(part + (block_id * block_sz));
    block->next = NULL;
    prev_block->next = block;
    prev_block = block;
  }
}

/**
 * bbos_mempool_alloc - Allocate next free memory block from the memory
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
bbos_mempool_alloc(bbos_mempool_id_t id)
{
  bbos_mempool_block_t *block;

  assert(id < BBOS_NUMBER_OF_MEMPOOLS); // check for NULL pointer

  /* Get next free memory block and move to the next one if possible */
  if ((block = bbos_mempool_table[id].next_free_block) != NULL) {
    bbos_mempool_table[id].next_free_block = block->next;
  }

  /* Return pointer to the next free memory block */
  return (void *)block;
}

/**
 * bbos_mempool_free - Return memory block to a memory pool.
 * @pool: Pointer to the used memory pool.
 * @addr: Pointer to the block.
 *
 * Complexity:
 *
 * O(1)
 */
void
bbos_mempool_free(bbos_mempool_id_t id, void *addr)
{
  bbos_mempool_block_t *block;

  assert(id < BBOS_NUMBER_OF_MEMPOOLS);

  /* Don't attempt to free a NULL pointer */
  if (addr == NULL) {
    return;
  }

  block = (bbos_mempool_block_t *)addr;

  /* Connect block with the chain of free blocks */
  block->next = bbos_mempool_table[id].next_free_block;
  bbos_mempool_table[id].next_free_block = block;
}


#endif

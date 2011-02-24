/*
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

#include <bbos/mm/mempool.h>
#include <assert.h>

/**
 * Initialize memory pool.
 *
 * \param part Pointer to the memory partition.
 * \param part_sz Partition size in bytes.
 * \param block_sz Block size in bytes.
 *
 * \return
 *
 * Pointer to the first free memory block.
 *
 * \note
 *
 * As close block size or number of blocks to the power of 2, as faster.
 *
 * It is the application's responsibility to manage the memory area
 * associated with the pool, which is available after this service completes.
 * In addition, the application must prevent use of a deleted pool or memory
 * previously allocated from it.
 */
void *
bbos_mempool_init(const void *part, uint16 part_sz, uint16 block_sz)
{
  assert(part);
	
  bbos_mempool_resize(part, part_sz, block_sz);
	
  return (void *)part;
}

/**
 * Resize an existed memory pool.
 *
 * \param part Pointer to the used memory partition.
 * \param part_sz Partition size in bytes.
 * \param block_sz Block size in bytes.
 */
void
bbos_mempool_resize(const void *part, uint16 part_sz, uint16 block_sz)
{
  uint16 i;
  void **prev;
  void **next;
	
  assert(part);

  uint16 n = part_sz / block_sz;

  for (i = 0; i < n; i++) {
    *(void **)(part + i * block_sz) = (void *)(part + (i + 1) * block_sz);
  }

  *(void **)(part + (i - 1) * block_sz) = NULL;
}

/**
 * Allocate next free memory block from the memory pool.
 *
 * \param pool Pointer to the target memory pool.
 *
 * \return
 *
 * Pointer to the memory block or NULL if there are no free blocks.
 *
 * \note
 *
 * O(1)
 */
void *
bbos_mempool_alloc(void **pool)
{
  void **block;

  assert(pool); // Check for NULL pointer

  BBOS_MEMPOOL_ALLOC(pool, block);

  return (void *)block;
}

/**
 * Return memory block to a memory pool.
 *
 * \param pool Pointer to the used memory pool.
 * \param block Pointer to the memory block.
 *
 * \note
 *
 * O(1)
 */
void
bbos_mempool_free(void **pool, void *block)
{
  assert(pool);		// Check for NULL pointer
  assert(block);	// Check for NULL pointer

  BBOS_MEMPOOL_FREE(pool, block);
}

// http://rt-thread.googlecode.com/svn/branches/rtt_0_3_2/src/mempool.c



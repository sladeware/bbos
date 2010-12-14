/*
 * Memory pool is a memory allocator with constant time access to dynamic
 * allocation for fixed-size chunks of memory.
 *
 * No footprint, just one void pointer to keep the pool.
 *
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

#include <bbos/mm/mempool.h>
#include <assert.h>

/**
 * bbos_mempool_init - Initialize memory pool.
 * @part: Pointer to the memory partition.
 * @n: Number of blocks in partition.
 * @sz: Number of bytes in each memory block.
 *
 * Return value:
 *
 * Pointer to the first free memory block.
 *
 * Note:
 *
 * As close block size or number of blocks to the power of 2, as faster.
 *
 * It is the application's responsibility to manage the memory area
 * associated with the pool, which is available after this service completes.
 * In addition, the application must prevent use of a deleted pool or memory
 * previously allocated from it.
 */
void *
bbos_mempool_init(const void *part, uint16 sz, uint16 l)
{
	assert(part);
	
	bbos_mempool_resize(part, sz, l);
	
	return (void *)part;
}

/**
 * bbos_mempool_resize - Resize an existed memory pool.
 * @part: Pointer to the used memory partition.
 * @n: Number of blocks in partition.
 * @sz: Block size in bytes.
 */
void
bbos_mempool_resize(const void *part, uint16 sz, uint16 l)
{
	uint16 i;
	void **prev;
	void **next;
	
	assert(part);

	uint16 n = sz / l;

	for (i = 0; i < n; i++) {
		*(void **)(part + i * l) = (void *)(part + (i + 1) * l);
	}
	*(void **)(part + (i - 1) * l) = NULL;
}

/**
 * bbos_mempool_alloc - Allocate next free memory block from the memory pool.
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
bbos_mempool_alloc(void **pool)
{
	void **chunk;

  assert(pool); // Check for NULL pointer

	BBOS_MEMPOOL_ALLOC(pool, chunk);

  return (void *)chunk;
}

/**
 * bbos_mempool_free - Return memory block to a memory pool.
 * @pool: Pointer to the used memory pool.
 * @chunk: Pointer to the memory chunk.
 *
 * Complexity:
 *
 * O(1)
 */
void
bbos_mempool_free(void **pool, void *chunk)
{
  assert(pool);		// Check for NULL pointer
  assert(block);	// Check for NULL pointer

	BBOS_MEMPOOL_FREE(pool, chunk);
}

// http://rt-thread.googlecode.com/svn/branches/rtt_0_3_2/src/mempool.c



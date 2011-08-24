/*
 * Copyright (c) 2011 Sladeware LLC
 */

#include <bb/mm/mempool.h>
#include <stddef.h>
#include <assert.h>

/**
 * Initialize memory pool.
 *
 * @param p Pointer to the memory partition.
 * @param n Number of blocks in partition
 * @param sz Block size in bytes
 *
 * @return Pointer to the first free memory block.
 *
 * @note
 *
 * As close block size @c sz or number of blocks @c n to the power of 2, as
 * faster.
 *
 * It is the application's responsibility to manage the memory area
 * associated with the pool, which is available after this service completes.
 * In addition, the application must prevent use of a deleted pool or memory
 * previously allocated from it.
 */
void*
bbos_mempool_init(const void* p, uint16_t n, uint16_t sz)
{
  assert(p);
  bbos_mempool_resize(p, n, sz);
  return (void *)p;
}

/**
 * Resize an existed memory pool.
 *
 * @param p Pointer to the used memory partition
 * @param n Number of blocks in partition
 * @param sz Block size in bytes
 */
void
bbos_mempool_resize(const void* p, uint16_t n, uint16_t sz)
{
  uint16_t i;
  void** prev;
  void** next;

  assert(p); /* Check for NULL pointer */

  for (i = 0; i < n; i++) {
    *(void**)(p + i * sz) = (void*)(p + (i + 1) * sz);
  }
  *(void **)(p + (i - 1) * sz) = NULL;
}

/**
 * Allocate next free memory block from the memory pool.
 *
 * @param p Pointer to the target memory pool.
 * @return Pointer to the memory block or @c NULL if there are no free blocks.
 *
 * @note O(1)
 */
void*
bbos_mempool_alloc(void** p)
{
  void** b;
  assert(p); /* Check for NULL pointer */
  BBOS_MEMPOOL_ALLOC(p, b);
  return (void *)b;
}

/**
 * Return memory block to a memory pool.
 *
 * @param p Pointer to the used memory pool
 * @param b Pointer to the memory block
 *
 * @note O(1)
 */
void
bbos_mempool_free(void** p, void* b)
{
  assert(p); /* Check for NULL pointer */
  assert(b); /* Check for NULL pointer */
  BBOS_MEMPOOL_FREE(p, b);
}

// http://rt-thread.googlecode.com/svn/branches/rtt_0_3_2/src/mempool.c

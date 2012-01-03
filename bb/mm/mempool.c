/*
 * Copyright (c) 2011 Sladeware LLC
 */

#include <bb/mm/mempool.h>
#include <stddef.h>
#include <assert.h>

/*
 * Initialize memory pool.
 *
 * Notice, as close block size sz or number of blocks n to the power of 2, as
 * faster.
 *
 * It is the application's responsibility to manage the memory area
 * associated with the pool, which is available after this service completes.
 * In addition, the application must prevent use of a deleted pool or memory
 * previously allocated from it.
 */
void*
mempool_init(const void* p, uint16_t n, uint16_t sz)
{
  bbos_assert(p);
  mempool_resize(p, n, sz);
  return (void *)p;
}

/* Resize an existed memory pool. */
void
mempool_resize(const void* p, uint16_t n, uint16_t sz)
{
  uint16_t i;
  void** prev;
  void** next;

  bbos_assert(p); /* Check for NULL pointer */

  for (i = 0; i < n; i++)
    {
      *(void**)(p + i * sz) = (void*)(p + (i + 1) * sz);
    }
  *(void **)(p + (i - 1) * sz) = NULL;
}

/* Allocate next free memory block from the memory pool. */
void*
mempool_alloc(void** p)
{
  void** b;
  bbos_assert(p); /* Check for NULL pointer */
  MEMPOOL_ALLOC(p, b);
  return (void *)b;
}

/* Return memory block to a memory pool. */
void
mempool_free(void** p, void* b)
{
  bbos_assert(p); /* Check for NULL pointer */
  bbos_assert(b); /* Check for NULL pointer */
  MEMPOOL_FREE(p, b);
}

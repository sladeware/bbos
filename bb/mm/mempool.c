/*
 * Memory pool.
 *
 * Copyright (c) 2012 Sladeware LLC
 */

#include <bb/mm/mempool.h>
#include <bb/config/stdlib/stddef.h>
#include <bb/assert.h>

/**
 * Initialize memory pool.
 *
 * @return
 *
 * Pointer to the first free memory block.
 *
 * @note
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
  BB_ASSERT(p);
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
  BB_ASSERT(p); /* Check for NULL pointer */
  for (i = 0; i < n; i++)
    {
#ifdef MEMPOOL_DEBUG
      printf("%d -> %d\n", i*sz, (i+1) * sz);
#endif
      *(void**)(p + i * sz) = (void*)(p + (i + 1) * sz);
    }
#ifdef MEMPOOL_DEBUG
  printf("%d -> 0\n", i * sz);
#endif
  /* *(void **)(p + (i - 1) * sz) = NULL; */
  *(void **)(p + i * sz) = NULL;
}

/* Allocate next free memory block from the memory pool. */
void*
mempool_alloc(void** p)
{
  void** b;
  BB_ASSERT(p); /* Check for NULL pointer */
  MEMPOOL_ALLOC(p, b);
  return (void *)b;
}

/* Return memory block to a memory pool. */
void
mempool_free(void** p, void* b)
{
  BB_ASSERT(p); /* Check for NULL pointer */
  BB_ASSERT(b); /* Check for NULL pointer */
  MEMPOOL_FREE(p, b);
}

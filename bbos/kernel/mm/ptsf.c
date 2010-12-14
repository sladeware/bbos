/*
 * Memory pool manager.
 *
 * This is an fixed sized allocation scheme which combines a power-of-two 
 * allocation with memory pools.
 * 
 *
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

#include <assert.h>
#include <stdio.h>
#include <bbos/kernel/types.h>
#include <bbos/kernel/log2.h>
#include <bbos/mm/mempool.h>
#include <bbos/mm/ptsf.h>

/*
 * Memory chunk identifier has the following view:
 *
 * +------------+-----------------------+
 * | CHUNK SIZE |     CHUNK POINTER     |
 * +------------+-----------------------+
 * 31           28                      0
 *
 * Use CHUNK_SIZE() macro to define chunk size and CHUNK_PTR() to get memory 
 * pointer.
 */

/*
 * The exponent for the power-of-two sized chunks of memory is referred to as 
 * the order. The bbos_mempool_order points to a linked list of chunks. Such  
 * linked list is formed by bbos_mempool interface, since the memory pool is 
 * just a void pointer to the next free chunk of memory.
 *
 * Hence, the 0th element of the bbos_mempool_map array will point to a list of
 * free chunks of size 2**0, the 1st element will be a list 2**1 and so up to
 * 2**(BBOS_MAX_ORDER-1).
 */
static void *_order[BBOS_MAX_ORDER];

/**
 * bbos_free - Deallocate memory chunk by its identifier.
 * @id: Memory chunk identifier.
 *
 * Notice:
 *
 * It's very important to have the chunk identifier but not just a pointer to
 * the allocated memory chunk. Otherwise, the chunk will not be released.
 */
void
bbos_free(void *id)
{
  assert(BBOS_CHUNK_SIZE(mem) < BBOS_MAX_ORDER);
  assert(ptsf_map[BBOS_CHUNK_SIZE(mem)] != NULL);

  bbos_mempool_free(ptsf_map[BBOS_CHUNK_SIZE(mem)], mem);
}

/**
 * bbos_malloc - Allocate memory chunk with specified size.
 * @sz: Memory chunk size.
 *
 * Return value:
 *
 * Memory chunk identifier.
 */
void *
bbos_malloc(size_t sz)
{
  uint16 order;
  void *pool;

  // Round down to the next power of 2, since our 'let the indices
  // wrap' technique works only in this case.
  if (!is_power_of_2(sz)) {
    sz = rounddown_pow_of_2(sz);
  }

  order = ilog2(sz);

  if (order <= BBOS_MAX_ORDER && (pool = _order[p]) != NULL) {
    return (void *)((uint32)bbos_mempool_alloc(pool) \
    	| ((uint32)(sz << BBOS_CHUNK_HEADER_BIT)));
  }
  
  return NULL;
}

void
bbos_mempool_register(void *pool, uint16 sz)
{
  uint16 p;

  p = ilog2(sz);
  
  // When the power of 2 associated with specified size of memory block is not 
  // on the map, the pool will be simply added. Otherwise, it will be merged 
  // with an existed one.
  if (ptsf_map[p] == NULL) {
    ptsf_map[p] = pool;
  }
  else {
    // bbos_mempool_merge(ptsf_map[p], pool);
  }
}



/*
 * Copyright (c) 2011 Sladeware LLC
 */

#ifndef __BB_MM_MEMPOOL_H
#define __BB_MM_MEMPOOL_H

/**
 * @file bb/mm/mempool.h
 * @brief Memory pool allocator
 *
 * @c mempool is fast memory allocator with constant time access to dynamic
 * allocation for fixed-size chunks of memory.
 *
 * <b>No footprint</b>, just one void pointer to keep the pool.
 *
   @b Synopsis

   @verbatim
#include <bb/config.h>
#include <bb/mm/mempool.h>

#define NUM_BLOCKS 10
#define BLOCK_SIZE 10

PRIVATE BBOS_MEMPOOL(buf, NUM_BLOCKS, BLOCK_SIZE);
PRIVATE int8_t* tests[NUM_BLOCKS];

int
main()
{
  void* pool;
  uint16_t i;
  int8_t* test;

  pool = bbos_mempool_init((void *)buf, NUM_BLOCKS, BLOCK_SIZE);
  for (i = 0; i < NUM_BLOCKS; i++) {
    if ((test = bbos_mempool_alloc(&pool)) == NULL) {
      printf("Can not allocate memory block from pool <%p>\n", pool);
      return 1;
    }
    sprintf(test, "Test #%d\n", i);
    tests[i] = test;
  }

  for (i = 0; i < NUM_BLOCKS; i++) {
    printf("%s\n", tests[i]);
    bbos_mempool_free(&pool, tests[i]);
  }

  return 0;
}
   @endverbatim
 */


#include <bb/config.h>
#include <bb/stdint.h>

/**
 * @def BBOS_MEMPOOL(name, n, sz)
 * @brief Create new memory partition with size @c n*sz bytes.
 * @param name Partition name
 * @param n Partition size in bytes.
 * @param sz Block size in bytes.
 */
#define BBOS_MEMPOOL(name, n, sz)               \
  int8_t name[n * sz]

/**
 * @def BBOS_MEMPOOL_ALLOC(pool, block)
 * @brief Allocate a block of memory from the pool. Basically used for better
 * performance.
 * @param pool Pointer to the used memory pool
 * @param block Pointer to the memory block
 * @see bbos_mempool_alloc()
 * @see BBOS_MEMPOOL_FREE()
 */
#define BBOS_MEMPOOL_ALLOC(pool, block)         \
  do {                                          \
    if ((block = (void**)*pool) != NULL) {      \
      *pool = *block;                           \
    }                                           \
  } while (0)

/**
 * @def BBOS_MEMPOOL_FREE(pool, block)
 * @brief Free a memory block.
 * @param pool Pointer to the used memory pool
 * @param block Pointer to the memory block
 */
#define BBOS_MEMPOOL_FREE(pool, block)          \
  do {                                          \
    if (block != NULL) {                        \
      *((void**)block) = *pool;                 \
      *pool = (void*)block;                     \
    }                                           \
  } while (0)

/* Prototypes */

PROTOTYPE(void* bbos_mempool_init, (const void* p, uint16_t n, uint16_t sz));
PROTOTYPE(void bbos_mempool_resize, (const void* p, uint16_t n, uint16_t sz));
PROTOTYPE(void* bbos_mempool_alloc, (void** p));
PROTOTYPE(void bbos_mempool_free, (void** p, void* b));

#endif /* __BB_MM_MEMPOOL_H */

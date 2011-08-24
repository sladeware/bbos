/*
 * Copyright (c) 2011 Sladeware LLC
 */

#ifndef __SIMPLE_SEGREGATED_STORAGE_H
#define __SIMPLE_SEGREGATED_STORATE_H

/**
 * @file bb/mm/simple_segregated_storage.h
 * @brief Simple segregated storage dynamic memory allocator
 *
 * With simple segregated storage, the free list for each size class contains
 * same-sized blocks, each the size of the largest element of the size class.
 * For example, if some size class is defined as (17 – 32), then the free list
 * for that class consists entirely of blocks of size 32.
 *
 * To allocate a block of some given size, we check the appropriate free list.
 * If the list is not empty, we simply allocate the first block in its entirety.
 * Free blocks are never split to satisfy allocation requests. If the list is
 * empty, the allocator returns @c NULL. To free a block, the allocator simply
 * inserts the block at the front of the appropriate free list.
 */

/**
 * @def MAX_ORDER
 * @brief Max size for the memory chunk is @c 2**MAX_ORDER.
 */
#define MAX_ORDER 16

/**
 * @def MAX_ORDER_LOG2
 * @brief log2(MAX_ORDER)
 */
#define MAX_ORDER_LOG2 4

/**
 * @def CHUNK_MASK
 * @brief Mask for 32-bit pointer.
 */
#define MASK 0xFFFFFFF

/**
 * @def CHUNK_HEADER_BIT
 * @brief The first bit where the header has to be stored. Equals to
 * @c (32 - MAX_ORDER_LOG2) .
 */
#define CHUNK_HEADER_BIT 28

/**
 * @def CHUNK_SIZE(id)
 * @param id Chunk identifier
 * @brief Obtain chunk size by its identifier.
 */
#define CHUNK_SIZE(id) \
  (((uint32)(id) & (uint32)(0x0000000F)) >> (uint32)(CHUNK_HEADER_BIT))

/**
 * @def HANDLE
 * @brief Take pointer to the chunk from the chunk identifier and cast it.
 * @param cast Cast the pointer.
 * @param id Chunk identifier.
 */
#define HANDLE(cast, id) \
   ((cast)((uint32)(id) & (uint32)(CHUNK_MASK)))

void bbos_associate_pool(void* pool, uint16 sz);
void *bbos_malloc(size_t sz);
void bbos_free(void* id);

#endif /* __SIMPLE_SEGREGATED_STORATE_H */

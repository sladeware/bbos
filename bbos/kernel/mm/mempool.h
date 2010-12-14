/*
 * Memory pool.
 *
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */
#ifndef __BBOS_MM_MEMPOOL_H
#define __BBOS_MM_MEMPOOL_H

#include <bbos/ansi.h>
#include <bbos/kernel/codes.h>
#include <bbos/kernel/types.h>

#ifdef __cplusplus
extern "C" {
#endif

/*
 * Computes size of the memory partition by using specified number
 * of blocks and block size.
 */
#define BBOS_MEMPOOL_PARTITION_SIZE(num_blocks, block_size) \
  (num_blocks * block_size)

/*
 * Creates memory partition with the specified name.
 */
#define BBOS_MEMPOOL_PARTITION(name, num_blocks, block_size)		\
  int8_t name[BBOS_MEMPOOL_PARTITION_SIZE(num_blocks, block_size)]

/* Macros */

#define BBOS_MEMPOOL_ALLOC(pool, block)	\
	do {	\
		if ((block = (void **)*pool) != NULL) {	\
			*pool = *block;	\
		}	\
	} while (0)

#define BBOS_MEMPOOL_FREE(pool, block)	\
	do {	\
		if (block != NULL) {	\
			*((void **)block) = *pool;	\
			*pool = (void *)block;	\
		}	\
	} while (0)

/* Prototypes */

PROTOTYPE(void *bbos_mempool_init(const void *part, uint16 n, uint16 sz));
PROTOTYPE(void bbos_mempool_resize(const void *part, uint16 n, uint16 sz));
PROTOTYPE(void *bbos_mempool_alloc(void **pool));
PROTOTYPE(void bbos_mempool_free(void **pool, void *block));

#ifdef __cplusplus
}
#endif

#endif /* __BBOS_MM_MEMPOOL_H */


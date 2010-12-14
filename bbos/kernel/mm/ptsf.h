/*
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_MM_PTSF_H
#define __BBOS_MM_PTSF_H

#include <bbos/kernel/types.h>
#include <bbos/ansi.h>

#define MAX_ORDER 16
#define MAX_ORDER_LOG2 4
#define MASK 0xFFFFFFF

// The first bit where the header has to be stored
#define CHUNK_HEADER_BIT 28 // 32-PTSF_MAX_ORDER_LOG2

// Obtain chunk size by its identifier
#define CHUNK_SIZE(id) (((uint32)(id) & (uint32)(0x0000000F)) >> (uint32)(CHUNK_HEADER_BIT))

#define PTSF_HANDLE(cast, id) ((cast)((uint32)(id) & (uint32)(MASK)))

PROTOTYPE(void bbos_associate_pool(void *pool, uint16 sz));
PROTOTYPE(void *bbos_malloc(size_t sz));
PROTOTYPE(void bbos_free(void *mem));

#endif



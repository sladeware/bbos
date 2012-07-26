/*
 * Simple segregated storage interface
 *
 * Copyright (c) 2011 Sladeware LLC
 */
#ifndef __SIMPLE_SEGREGATED_STORAGE_H
#define __SIMPLE_SEGREGATED_STORAGE_H

/* Used to compute max size for the memory chunk: 2**MAX_ORDER */
#define MAX_ORDER 16

#define MAX_ORDER_LOG2 4 /* log2(MAX_ORDER) */

/* Mask for 32-bit pointer */
#define MAX 0xffffffff

/*  */

#endif /* __SIMPLE_SEGREGATED_STORAGE_H */

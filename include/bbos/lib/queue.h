/*
 * Queue, a First-In-First-Out (FIFO) data structure.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_LIB_QUEUE_H
#define __BBOS_LIB_QUEUE_H

#include <stddef.h>
#include <bbos/env.h>

/* Queue structure */
typedef struct {
  /* Pointer to the used memory partition */
  size_t *addr;

  /* Tracks number of elements in the queue */
  uint16_t counter;

  /* Index of the first free element */
  uint16_t first;

  /* Index of the last free element */
  uint16_t last;

  /* Queue length */
  uint16_t len;
} bbos_queue_t;

enum {
	BBOS_QUEUE_OVERHEAD = ((int16_t)sizeof(bbos_queue_t))
};

/**
 * Computes the size of memory requred to keep queue elements (in bytes).
 */
#define BBOS_QUEUE_PARTITION_SIZE(n)		\
  (BBOS_QUEUE_OVERHEAD + (sizeof(size_t) * n))

/**
 * Returns the total number of elements in the queue.
 */
#define bbos_queue_size(q)			\
  ((q)->counter)

/**
 * Returns true if queue is empty.
 */
#define bbos_queue_empty(q)			\
  (!(q)->counter)

/* Prototypes */

bbos_queue_t *bbos_queue_init(void *part, uint16_t n);
void *bbos_queue_dequeue(bbos_queue_t *q);
bbos_return_t bbos_queue_enqueue(bbos_queue_t *q, void *ptr);
int16_t bbos_queue_full(bbos_queue_t *q);

#endif /* __BBOS_LIB_QUEUE_H */


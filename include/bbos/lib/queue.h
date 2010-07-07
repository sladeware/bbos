/*
 * Queue data structure.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_LIB_QUEUE_H
#define __BBOS_LIB_QUEUE_H

#include <bbos/lib/list.h>

typedef list_t queue_t;

/**
 * Computes the size of memory requred to keep queue elements (in bytes).
 */
#define QUEUE_PARTITION_SIZE(n)	LIST_PARTITION_SIZE(n)

#define QUEUE_PARTITION(name, n) LIST_PARTITION(name, n)

#define queue_init list_init

#define queue_peek(queue) ((queue)->head == NULL ? NULL : (queue)->head->data) 

#define queue_counter list_counter

bbos_return_t queue_enqueue(queue_t *queue, const void *data); 

void *queue_dequeue(queue_t *queue); 

#endif /* __BBOS_LIB_QUEUE_H */


/*
 * Queue data structure.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_QUEUE_H
#define __BBOS_QUEUE_H

#ifdef __cplusplus
extern "C" {
#endif

typedef bbos_list_t bbos_queue_t;

/*
 * Compute the size of memory requred to keep queue elements (in bytes).
 */
#define BBOS_QUEUE_PARTITION_SIZE(n) BBOS_LIST_PARTITION_SIZE(n)

/*
 * Create the new queue with name `name' and required number of elements `n'.
 */
#define BBOS_QUEUE_PARTITION(name, n) BBOS_LIST_PARTITION(name, n)

#define bbos_queue_init bbos_list_init
#define bbos_queue_destroy bbos_list_destroy

#define bbos_queue_peek(queue) ((queue)->head == NULL ? NULL : (queue)->head->data)

#define bbos_queue_counter bbos_list_counter

bbos_return_t bbos_queue_enqueue(bbos_queue_t *queue, const void *data);

void *bbos_queue_dequeue(bbos_queue_t *queue);

#ifdef __cplusplus
}
#endif

#endif /* __BBOS_QUEUE_H */


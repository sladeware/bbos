/*
 * Queue data structure.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#include <bbos.h>

/**
 * bbos_queue_enqueue - Enqueues an element at the tail of the queue.
 * @queue: Pointer to the queue data structure.
 * @data: Pointer to the data.
 *
 * Return value:
 *
 * BBOS_SUCCESS if enqueuing the element is successful, or BBOS_FAILURE otherwise.
 *
 * Complexity:
 *
 * O(1)
 */
bbos_return_t
bbos_queue_enqueue(bbos_queue_t *queue, const void *data)
{
  return bbos_list_insert(queue, bbos_list_tail(queue), data);
}

/**
 * bbos_queue_dequeue - Dequeues an element from the head of the queue.
 * @queue: Pointer to the queue data structure.
 *
 * Return value:
 *
 * Pointer to the data, or NULL otherwise.
 *
 * Complexity:
 *
 * O(1)
 *
 * TODO:
 *
 * Pointer to an error can be added as an argument.
 */
void *
bbos_queue_dequeue(bbos_queue_t *queue)
{
  return bbos_list_remove(queue, NULL);
}


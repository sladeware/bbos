/*
 * Queue, a First-In-First-Out (FIFO) data structure.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#include <bbos/lib/bbos_queue.h>

/**
 * bbos_queue_full - Check whether queue is full or not.
 * @q: Pointer to the queue structure.
 *
 * Return value:
 *
 * Returns true if the queue is full, and false otherwise.
 */
int16_t
bbos_queue_full(bbos_queue_t *q)
{
  assert(q); // check queue for NULL pointer

  return !(q->len - q->counter);
}

/**
 * bbos_queue_init - Define whether queue is empty or not.
 * @part: Pointer to the memory partition.
 * @n: Number of elements in the queue.
 *
 * Return value:
 *
 * Pointer to the queue structure.
 */
bbos_queue_t *
bbos_queue_init(void *part, uint16_t n)
{
  bbos_queue_t *q;

  assert(part);

  q = (bbos_queue_t *)part;
  q->addr = (size_t *)((int8_t *)part + BBOS_QUEUE_OVERHEAD);
  q->counter = 0;
  q->first = q->last = 0;
  q->len = n;

  return q;
}

/**
 * bbos_queue_dequeue - Remove the item at the front of a queue and return it.
 * @q: Pointer to the queue structure.
 *
 * Return value:
 * Pointer to the element or NULL.
 */

void *
bbos_queue_dequeue(bbos_queue_t *q)
{
  void *ptr;

  assert(q);

  if(bbos_queue_empty(q)) {
    return NULL;
  }

  ptr = (void *)q->addr[q->first];
  q->first = (q->first + 1) % q->len;
  q->counter--;

  return (void *)ptr;
}

/**
 * bbos_queue_enqueue - Insert an element at the back of the queue.
 * @q: Pointer to the queue structure.
 * @ptr: Pointer to the element.
 *
 * Return value:
 *
 *   BBOS_SUCCESS   success.
 *   BBBOS_FAILURE  fail.
 */
bbos_return_t
bbos_queue_enqueue(bbos_queue_t *q, void *ptr)
{
  assert(q);

  if(bbos_queue_full(q)) {
    return BBOS_FAILURE;
  }

  q->addr[q->last] = (size_t)ptr;
  q->last = (q->last + 1) % q->len;
  q->counter++;

  return BBOS_SUCCESS;
}

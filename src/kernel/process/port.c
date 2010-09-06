/*
 * Port.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#include <bbos.h>

/*
 * The port interface will not be provided, unless at least 1 port will not be 
 * defined.
 */
#if BBOS_NUMBER_OF_PORTS > 0

/**
 * bbos_port_init - Initialize the target port.
 * @port_id: Port identifier.
 * @part: Pointer to the memory partition.
 * @n: Number of blocks that a port can hold.
 * @sz: Size of a single block in bytes.
 *
 * Complexity:
 *
 * O(2n), where n is the number of blocks.
 */
void
bbos_port_init(bbos_port_id_t port_id, void *part, uint16_t n, uint16_t sz)
{
  assert(port_id < BBOS_NUMBER_OF_PORTS);
  assert(part); // check for a NULL pointer

  /* Initialize queue of blocks */
  bbos_process_port_table[port_id].queue = bbos_queue_init(part, n);

  /* Initialize buffer */
  bbos_process_port_table[port_id].buffer =
  bbos_mempool_init((int8_t *)part + BBOS_QUEUE_PARTITION_SIZE(n), n, sz);
}

/**
 * bbos_port_alloc - Allocate memory for communication with the target port.
 * @port_id: Port identifier.
 *
 * Return value:
 *
 * Pointer to the memory block or NULL.
 */
void *
kernel_port_alloc(bbos_port_id_t port_id)
{
  assert(port_id < BBOS_NUMBER_OF_PORTS);

  /* Allocate an amount of memory from a buffer */
  return bbos_mempool_alloc(bbos_process_port_table[port_id].buffer);
}

/**
 * bbos_port_enqueue - Enqueue the memory block into the port's queue.
 * @port_id: Port identifier.
 * @block: Pointer to the memory block.
 *
 * Note:
 *
 * The memory block should be allocated from the same port.
 *
 * Return value:
 *
 * BBOS_SUCCESS if enqueuing the element is successful, or BBOS_FAILUR otherwise.
 *
 * Complexity:
 *
 * O(1)
 */
bbos_return_t
bbos_port_enqueue(bbos_port_id_t port_id, void *block)
{
  assert(port_id < BBOS_NUMBER_OF_PORTS);

  if(block == NULL) {
    return BBOS_FAILURE;
  }

  return queue_enqueue(bbos_process_port_table[port_id].queue, block);
}

/**
 * bbos_port_dequeue - Dequeue the memory block.
 * @port_id: Port identifier.
 * @block: Pointer to the block.
 *
 * Return value:
 *
 * Pointer to the memory block or NULL if it's empty.
 *
 * Complexity:
 *
 * O(1)
 */
void *
bbos_port_dequeue(bbos_port_id_t port_id)
{
  assert(port_id < BBOS_NUMBER_OF_PORTS);

  return queue_dequeue(bbos_process_port_table[port_id].queue);
}

/**
 * bbos_port_free - Free the memory block.
 * @port_id: Port identifier.
 * @block: Pointer to the memory block.
 *
 * Complexity:
 *
 * O(1)
 */
void
bbos_port_free(bbos_port_id_t port_id, void *block)
{
  assert(port_id < BBOS_NUMBER_OF_PORTS);

  /* Delete the message data */
  bbos_mempool_free(bbos_process_port_table[port_id].buffer, block);
}

#endif /* BBOS_NUMBER_OF_PORTS > 0 */

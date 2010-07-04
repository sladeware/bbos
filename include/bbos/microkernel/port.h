/*
 * The communication port interface.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_MICROKERNEL_PORT_H
#define __BBOS_MICROKERNEL_PORT_H

#include <bbos/env.h>
#include <bbos/lib/bbos_queue.h>
#include <bbos/lib/memory/bbos_mempool.h>

/** Some well known thread id's. */
#define BBOS_NIL_PORT_ID 0xFF

/**
 * struct bbos_port - The port structure.
 * @queue: Queue of the port messages.
 * @buffer: Pointer to the memory buffer for the message data.
 */
struct bbos_port {
  bbos_queue_t *queue;
  bbos_mempool_t *buffer;
};

/** 
 * typedef bbos_port_t - The port data type.
 */
typedef struct bbos_port bbos_port_t;

/**
 * BBOS_PORT_PARTITION_SIZE - Calculates the size (in bytes) of required 
 * memory partition which will be taken by the port.
 * @n: Number of message.
 * @sz: Message size.
 */
#define BBOS_PORT_PARTITION_SIZE(n, sz)					\
  (BBOS_QUEUE_PARTITION_SIZE(n) + BBOS_MEMPOOL_PARTITION_SIZE(n, sz))	\

/**
 * BBOS_PORT - Create a port's memory partition.
 * @name: Port name.
 * @n: Number of messages supported by this port.
 * @sz: Size of a message.
 *
 * The port needs to be created before it can be used. Creating a port is
 * accomplished by calling BBOS_PORT() macro and specifying the number of
 * messages and the size of single one.
 */
#define BBOS_PORT(name, n, sz)			\
  int8_t name[BBOS_PORT_PARTITION_SIZE(n, sz)]

/* Prototypes */

void bbos_port_init(bbos_port_id_t pid, void *part, uint16_t n, uint16_t sz);

void *bbos_port_alloc(bbos_port_id_t pid);

void bbos_port_free(bbos_port_id_t pid, void *block);

bbos_return_t bbos_port_enqueue(bbos_port_id_t pid, void *block);

void *bbos_port_dequeue(bbos_port_id_t pid);

#endif /* __BBOS_MICROKERNEL_PORT_H */


/*
 * Inter-Thread Communication.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_MICROKERNEL_ITC_H
#define __BBOS_MICROKERNEL_ITC_H

#include <bbos/env.h>
#include <bbos/microkernel/thread.h>
#include <bbos/microkernel/port.h>

/**
 * struct bbos_itc_header - The ITCs message header structure.
 * @sender: Who sent the message.
 * @source_port_id: The port from which message was sent.
 * @return_port_id: The port which can be used to reply.
 * @message: Pointer to the message data.
 *
 * The message header structure describes the header which will be used with
 * each message to identify it within BBOS system.
 */
struct bbos_itc_header {
  bbos_thread_id_t sender;
  bbos_port_id_t source_port_id;
  bbos_port_id_t return_port_id;
  void *message;
};

/**
 * typedef bbos_itc_header_t - The message header data type.
 */
typedef struct bbos_itc_header bbos_itc_header_t;

enum {
  BBOS_ITC_HEADER_OVERHEAD = ((int16_t)sizeof(bbos_itc_header_t))
};

#define BBOS_ITC_GET_MESSAGE_HEADER(msg)			\
  (bbos_itc_header_t *)((int8_t *)msg - BBOS_ITC_HEADER_OVERHEAD)

/**
 * BBOS_ITC_PORT - Create an ITC port's memory partition.
 * @name: Port name.
 * @n: Number of messages supported by this port.
 * @sz: Size of a message.
 *
 * The message size will be the actuall size plus the size of the ITC header(
 * see bbos_itc_header_t).
 */
#define BBOS_ITC_PORT(name, n, sz)		\
  BBOS_PORT(name, n, sz + BBOS_ITC_HEADER_OVERHEAD)

/* Prototypes */

void *bbos_itc_compose(bbos_port_id_t port_id);

void bbos_itc_set_return_port(void *msg, bbos_port_id_t port_id);

bbos_port_id_t bbos_itc_get_return_port(void *msg);

void *bbos_itc_reply(void *msg);

bbos_thread_id_t bbos_itc_get_sender(void *msg);

bbos_return_t bbos_itc_send(void *msg);

void *bbos_itc_receive(bbos_port_id_t port_id);

void bbos_itc_delete(void *msg);

#endif /* __BBOS_MICROKERNEL_ITC_H */


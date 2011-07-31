/*
 * Copyright (c) 2011 Sladeware LLC
 */

#ifndef __BBOS_PORT_H
#define __BBOS_PORT_H

/**
 * @file port.h
 * @brief Message port communication interface for efficient and flexible 
 * inter-thread communication
 *
 * Threads communicate with each other via message passing, where the message 
 * can be any data value. Message passing is @b asynchronous: a sending thread 
 * will not be suspended after sending a message. Sending a message will never 
 * fail; so if you try sending a message to nonexistent thread, it's thrown away
 * without generating an error. Also the sending thread cannot fail, even if the
 * receiving thread fails or becomes inaccessible. 
 *
 * The messages are sent to and received from the mailboxes called ports. All the
 * threads have their own ports. All the messages represented by a queue, where 
 * each thread keeps the head and tail of such queue. Thus the BBOS thread does 
 * not have own space for its port, and so, the number of messages is unlimited,
 * which means a queue of messages will never be full.
 *
 * Only two primitives are needed for message transfer. The bbos_port_send() 
 * primitive sendes a message to a thread. A message is received via 
 * bbos_port_receive().
 *
 * Since the thread does not have own memory to keep the messages, this memory 
 * has to be allocated by developer.
 *
 * Messages are stored in the list of messages in the order in which they are 
 * delivered. At the same time messages are retrieved @b selectively, so it's 
 * not necessary to process messages in the order they are received. This makes 
 * the concurrency more robust.
 */

#include <bb/os/kernel/types.h>

bbos_error_t bbos_port_send(bbos_thread_id_t receiver, bbos_message_t *message,
                            bbos_thread_id_t owner);

bbos_error_t bbos_port_receive(bbos_thread_id_t tid, bbos_message_t *message);

void bbos_port_flush(bbos_thread_id_t tid);

bbos_message_number_t bbos_port_is_empty(bbos_thread_id_t tid);

#endif


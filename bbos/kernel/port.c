/*
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

#include <bbos/config.h>
#include <bbos/kernel/port.h>
#include <bbos/kernel/error_codes.h>
#include <stdio.h>

static bbos_port_t bbos_port_table[BBOS_NUMBER_OF_THREADS];

/**
 * Defines whether the port is empty. If the port is not empty, returns number
 * of messages inside.
 *
 * @param tid Thread identifier.
 *
 * @return
 *
 * Number of messages.
 */
bbos_message_number_t
bbos_port_is_empty(bbos_thread_id_t tid)
{
  return bbos_port_table[tid].count;
}

/**
 * Basic primitive for sending. Send message to the thread's port.
 *
 * @param receiver Receiver's thread identifier.
 * @param message Pointer to the message.
 * @param owner Owner's thread identifier.
 *
 * @return
 *
 * Kernel error code.
 */
bbos_error_t
bbos_port_send(bbos_thread_id_t receiver, bbos_message_t *message, 
               bbos_thread_id_t owner)
{
  if (bbos_port_table[receiver].tail == NULL)
    {
      bbos_port_table[receiver].head = message;
      bbos_port_table[receiver].tail = message;
      message->next = NULL;
      return BBOS_SUCCESS;
    }

  message->next = bbos_port_table[receiver].tail->next;
  bbos_port_table[receiver].tail->next = message;
  
  message->owner = owner;
  
  return BBOS_SUCCESS;
}

/**
 * Basic primitive for receiving. Receive a message from the thread's port.
 *
 * @param tid Thread identifier.
 * @param message Pointer to the message.
 *
 * @return
 *
 * Kernel error code.
 */
bbos_error_t
bbos_port_receive(bbos_thread_id_t tid,
                  bbos_message_t *message)
{
  if (bbos_port_table[tid].head == NULL)
    return BBOS_FAILURE;

  *message = *bbos_port_table[tid].head;

  if (bbos_port_table[tid].head == bbos_port_table[tid].tail)
    bbos_port_table[tid].tail = NULL;
  else
    bbos_port_table[tid].head = bbos_port_table[tid].head->next;

  return BBOS_SUCCESS;
}

/**
 * Flush the port.
 *
 * @param tid Thread identifier.
 */
void
bbos_port_flush(bbos_thread_id_t tid)
{
  bbos_port_table[tid].head = bbos_port_table[tid].tail = NULL;
  bbos_port_table[tid].count = 0;
}


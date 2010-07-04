/*
 * File: itc.c
 * Description: Inter-thread communication.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#include <bbos/microkernel/itc.h>
#include <bbos/microkernel/process.h>
#include <bbos/microkernel/sched.h>

/**
 * bbos_itc_compose - Compose a new message.
 * @port_id: Port identifier.
 *
 * Return value:
 *
 * Pointer to the message data.
 */
void *
bbos_itc_compose(bbos_port_id_t port_id)
{
  bbos_itc_header_t *hdr;

  assert(port_id <= BBOS_NUMBER_OF_PORTS); // check id

  hdr = (bbos_itc_header_t *)bbos_port_alloc(port_id);
  if(hdr == NULL) { /* the target port is full */
    return NULL;
  }

  /* Form the message header */
  hdr->sender = bbos_sched_myself();
  hdr->source_port_id = port_id;
  hdr->return_port_id = BBOS_NIL_PORT_ID;

  return (hdr->message = (void *)((int8_t *)hdr + BBOS_ITC_HEADER_OVERHEAD));
}

/**
 * bbos_itc_set_return_port - Set return port.
 * @msg: Pointer to the message data.
 * @return_port: Return port.
 */
void
bbos_itc_set_return_port(void *msg, bbos_port_id_t port_id)
{
  bbos_itc_header_t *hdr;

  assert(port_id < BBOS_NUMBER_OF_PORTS);
  assert(msg);

  hdr = BBOS_ITC_GET_MESSAGE_HEADER(msg);
  hdr->return_port_id = port_id;
}

/**
 * bbos_itc_get_return_port - Get return port identifier.
 * @msg: Pointer to the message data.
 *
 * Return value:
 *
 * Returns identifier of the return port.
 */
bbos_port_id_t
bbos_itc_get_return_port(void *msg)
{
  bbos_itc_header_t *hdr;
  assert(msg);

  hdr = BBOS_ITC_GET_MESSAGE_HEADER(msg);
  return (hdr->return_port_id);
}

/**
 * bbos_itc_reply - Compose a new message as response on another.
 * @msg: Pointer to the message.
 *
 * Return value:
 *
 * Pointer to the message. Return NULL if reply is not allowed.
 */
void *
bbos_itc_reply(void *msg)
{
  bbos_itc_header_t *hdr;

  /* Nothing to reply */
  if(msg == NULL) {
    return NULL;
  }

  hdr = BBOS_ITC_GET_MESSAGE_HEADER(msg);

  /* The return port was not set, so the reply is not allowed */
  if(hdr->return_port_id == BBOS_NIL_PORT_ID) {
    return NULL;
  }

  /* The return port will be checked by bbos_itc_compose service */
  return bbos_itc_compose(hdr->return_port_id);
}

/**
 * bbos_itc_get_sender - Get sender identifier.
 * @msg: Pointer to the message.
 *
 * Return value:
 *
 * Thread identifier.
 */
bbos_thread_id_t
bbos_itc_get_sender(void *msg)
{
  bbos_itc_header_t *hdr;

  assert(msg);

  hdr = BBOS_ITC_GET_MESSAGE_HEADER(msg);
  return hdr->sender;
}

/**
 * bbos_itc_send - Send a message.
 * @msg: Pointer to the message data.
 *
 * Return value:
 *
 *   BBOS_SUCCESS  Success.
 *   BBOS_FAILURE  Fail.
 */
bbos_return_t
bbos_itc_send(void *msg)
{
  bbos_itc_header_t *hdr;

  if(msg == NULL) {
    return BBOS_FAILURE;
  }

  /* Get the message header */
  hdr = BBOS_ITC_GET_MESSAGE_HEADER(msg);

  /* Send a message to the appropriate port and return a feedback */
  return bbos_port_enqueue(hdr->source_port_id, msg);
}

/**
 * bbos_itc_delete - Delete a message.
 * @msg: Pointer to the message data.
 */
void
bbos_itc_delete(void *msg)
{
  bbos_itc_header_t *hdr;

  assert(msg);

  hdr = BBOS_ITC_GET_MESSAGE_HEADER(msg);

  /* Release used memory from the used buffer */
  bbos_port_free(hdr->source_port_id, hdr);
}

/**
 * bbos_itc_receive - Receive a new message for the target port.
 * @port_id: Port identifier.
 *
 * Return value:
 *
 * Pointer to the message.
 */
void *
bbos_itc_receive(bbos_port_id_t port_id)
{
  assert(port_id < BBOS_NUMBER_OF_PORTS);

  return (void *)bbos_port_dequeue(port_id);
}

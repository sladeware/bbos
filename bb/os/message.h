/*
 * Message interface.
 *
 * Copyright(c) 2012 Sladeware LLC
 * Author: Oleksandr Sviridenko
 */
#ifndef __BB_OS_MESSAGE_H
#define __BB_OS_MESSAGE_H

#include "thread.h"

typedef uint16_t bbos_message_label_t;
typedef void* bbos_message_payload_t;

struct bbos_message {
  bbos_message_label_t label; /* what kind of message is it */
  bbos_message_payload_t payload;
};

typedef struct bbos_message bbos_message_t;

struct bbos_message_record {
  bbos_thread_id_t owner;
  bbos_message_t message;
};

typedef struct bbos_message_record bbos_message_record_t;

/* Returns message owner's ID. */
#define BBOS_MESSAGE_GET_OWNER(msg) ((bbos_message_header_t*)(msg - sizeof(bbos_message_header_t)))->owner
#define BBOS_MESSAGE_GET_ID(msg) (msg)->id

/* NOTE: BBOS_MESSAGE_* macros require pointer on the message. */

#endif /* __BB_OS_MESSAGE_H */

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

struct bbos_message {
  bbos_thread_id_t sender;
  bbos_message_label_t label; /* what kind of message is it */
  void* payload;
};

typedef struct bbos_message bbos_message_t;

/* Returns message owner's ID. */
#define BBOS_MESSAGE_GET_LABEL(msg) (msg)->label
#define BBOS_MESSAGE_GET_SENDER(msg) (msg)->sender

/* NOTE: BBOS_MESSAGE_* macros require pointer on the message. */

#endif /* __BB_OS_MESSAGE_H */

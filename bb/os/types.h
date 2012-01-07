/*
 * Copyright (c) 2012 Sladeware LLC
 */
#ifndef __BBOS_TYPES_H
#define __BBOS_TYPES_H

typedef int16_t bbos_code_t;

typedef unsigned bbos_port_id_t;

typedef struct bbos_message {
  bbos_port_id_t owner; /**< Who owns the message. */
  int command; /**< What kind of message is it. */
  void* data; /**< Pointer to the message data. */
#ifdef BBOS_CONFIG_UNLIMIT_PORT_SIZE
  struct bbos_message* next; /**< Pointer to the next message in the queue.*/
#endif
} bbos_message_t;

typedef struct {
#ifdef BBOS_CONFIG_UNLIMIT_PORT_SIZE
  bbos_message_t* head; /**< Pointer to the last message in the list. */
  bbos_message_t* tail; /**< Pointer to the last message in the list. */
#else
  bbos_message_t** message_pool;
  int head;
  int tail;
#endif /* BBOS_CONFIG_UNLIMIT_PORT_SIZE */
  int counter;
  unsigned size; /* TODO: size_t */
} bbos_port_t;

/* Thread identifier represents up to 255 threads. */
typedef uint8_t bbos_thread_id_t;

/* Thread execution data type. */
typedef void (*bbos_thread_runner_t)(void);

typedef struct bbos_thread {
  bbos_port_id_t port_id; /* Port ID for communication */
  bbos_thread_runner_t runner; /* Pointer to the target function to be called */
} bbos_thread_t;

typedef struct bbos_device {
} bbos_device_t;

typedef int32_t bbos_device_id_t;

#endif /* __BBOS_TYPES_H */

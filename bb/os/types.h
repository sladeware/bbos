/*
 * Copyright (c) 2011 Sladeware LLC
 */
#ifndef __BBOS_TYPES_H
#define __BBOS_TYPES_H

typedef int16_t bbos_code_t;

typedef unsigned bbos_port_id_t;
typedef struct bbos_port {
} bbos_port_t;

/* Thread identifier represents up to 255 threads. */
typedef uint8_t bbos_thread_id_t;

/* Thread execution data type. */
typedef void (*bbos_thread_target_t)(void);

typedef struct bbos_thread {
  bbos_port_id_t port_id; /* Port identifier for communication */
  bbos_thread_target_t target; /* Pointer to the target function to be called */
} bbos_thread_t;

typedef struct bbos_message {
  bbos_port_id_t owner;
  bbos_port_id_t sender;
  int command;
  void* data;
} bbos_message_t;

typedef struct bbos_device {
} bbos_device_t;

typedef int32_t bbos_device_id_t;

#endif /* __BBOS_TYPES_H */

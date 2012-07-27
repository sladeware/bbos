// Copyright (c) 2012 Sladeware LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//       http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
// Author: Oleksandr Sviridenko

#ifndef __BB_OS_TYPES_H
#define __BB_OS_TYPES_H

typedef int16_t bbos_code_t;

typedef unsigned bbos_port_id_t;

typedef struct bbos_message {
  bbos_port_id_t owner; // who owns the message
  int command; // what kind of message is it
  void* data; // pointer to the message data
#ifdef BBOS_CONFIG_UNLIMIT_PORT_SIZE
  struct bbos_message* next; // pointer to the next message in the queue
#endif
} bbos_message_t;

typedef struct {
#ifdef BBOS_CONFIG_UNLIMIT_PORT_SIZE
  bbos_message_t* head; // pointer to the last message in the list
  bbos_message_t* tail; // pointer to the last message in the list
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
  bbos_port_id_t port_id; // port ID for communication
  bbos_thread_runner_t runner; // pointer to the target function to be called
} bbos_thread_t;

/*
typedef struct bbos_device {
} bbos_device_t;
*/

typedef int32_t bbos_device_id_t;

#endif // __BB_OS_TYPES_H

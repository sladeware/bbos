/*
 * Copyright (c) 2012 Sladeware LLC
 * Author: Oleksandr Sviridenko
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *       http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#ifndef __BB_OS_TYPES_H
#define __BB_OS_TYPES_H

typedef struct bbos_message {
  //bbos_port_id_t owner; /* who owns the message */
  int command; /* what kind of message is it */
  void* data; /* pointer to the message data */
#ifdef BBOS_CONFIG_UNLIMIT_PORT_SIZE
  struct bbos_message* next; // pointer to the next message in the queue
#endif
} bbos_message_t;

#endif /* __BB_OS_TYPES_H */

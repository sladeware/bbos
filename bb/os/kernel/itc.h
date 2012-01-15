/*
 * Inter-Thread Communication mechanism.
 *
 * Copyright (c) 2012 Sladeware LLC
 */
#ifndef __BBOS_KERNEL_ITC_H
#define __BBOS_KERNEL_ITC_H
#define BBOS_KERNEL_ITC

#include <bb/os/config.h>
#include <bb/mm/mempool.h>

/*******************************************************************************
 * The following primitives extends kernel functionality in order
 * to support messaging and ITC mechanism.
 ******************************************************************************/

extern bbos_port_t bbos_kernel_ports[BBOS_NR_PORTS];
extern int8_t bbos_kernel_messaging_part[];
extern void* bbos_kernel_messaging_pool;

/**
 * Select port by its identifier. Please use this primitive instead of
 * direct access to bbos_kernel_ports table.
 */
#define bbos_kernel_get_port(pid)               \
  bbos_kernel_ports[pid]

PROTOTYPE(bbos_message_t* bbos_kernel_receive_message, ());
PROTOTYPE(bbos_message_t* bbos_kernel_receive_message_from,
          (bbos_thread_id_t sender));
PROTOTYPE(bbos_code_t bbos_kernel_send_message, (bbos_message_t* message,
                                                 bbos_port_id_t pid));
PROTOTYPE(bbos_message_t* bbos_kernel_alloc_message, ());
PROTOTYPE(void bbos_kenrnel_free_message, (bbos_message_t* message));
PROTOTYPE(void bbos_kernel_init_itc, ());

#ifdef BBOS_CONFIG_UNLIMIT_PORT_SIZE
#define bbos_kernel_init_port(pid, sz, mp)      \
  __bbos_kernel_init_port(pid, sz)
PROTOTYPE(void __bbos_kernel_init_port, (bbos_port_id_t pid,
                                         int32_t sz));
#else
PROTOTYPE(void bbos_kernel_init_port, (bbos_port_id_t pid,
                                       int32_t sz,
                                       bbos_message_t** mp));
#endif /* BBOS_CONFIG_UNLIMIT_PORT_SIZE */

/*******************************************************************************
 * Ports
 */

#ifndef BBOS_CONFIG_MESSAGING_POOL_SIZE
#error
#endif

#define bbos_port_get_size(pid)                 \
  bbos_kernel_get_port(pid).size

/**
 * Define whether port is empty or does it has any messages.
 */
#define bbos_port_is_empty(pid)                 \
  (!bbos_kernel_get_port(pid).counter)

#define bbos_port_is_full(pid)                                      \
  (bbos_kernel_get_port(pid).counter == bbos_port_get_size(pid))

#define bbos_port_set_message_pool(pid, msgpool)        \
  do                                                    \
    {                                                   \
      bbos_kernel_get_port(pid).message_pool = msgpool; \
    }                                                   \
  while (0)

/**
 * Compare port identifier with supported number of ports
 * BBOS_NR_PORTS.
 */
#define bbos_validate_port_id(pid) assert(pid < BBOS_NR_PORTS)

PROTOTYPE(bbos_code_t bbos_port_push_message, (bbos_port_id_t pid,
                                               bbos_message_t* message));
PROTOTYPE(bbos_message_t* bbos_port_fetch_message, (bbos_port_id_t pid));

#endif /* __BBOS_KERNEL_ITC_H */

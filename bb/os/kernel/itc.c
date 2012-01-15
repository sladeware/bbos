/*
 * Copyright (c) 2012 Sladeware LLC
 */

#include <bb/os/kernel.h>
#include <bb/os/kernel/itc.h>

bbos_port_t bbos_kernel_ports[BBOS_NR_PORTS];
void* bbos_kernel_messaging_pool;

/*
 * Create global messaging pool which holds required number of
 * messages.
 */
MEMPOOL_PARTITION(bbos_kernel_messaging_part,
                  BBOS_CONFIG_MESSAGING_POOL_SIZE,
                  sizeof(bbos_message_t));

/**
 * Main ITC initialization entry point. Called once from
 * bbos_kernel_init() function.
 */
void
bbos_kernel_init_itc()
{
  bbos_kernel_messaging_pool = mempool_init(bbos_kernel_messaging_part,
                                            BBOS_CONFIG_MESSAGING_POOL_SIZE,
                                            sizeof(bbos_message_t));
}

bbos_code_t
bbos_kernel_send_message(bbos_message_t* message,
                         bbos_port_id_t pid)
{
  message->owner = bbos_thread_get_port_id(bbos_sched_identify_myself());
  return bbos_port_push_message(pid, message);
}

bbos_message_t*
bbos_kernel_receive_message()
{
  bbos_port_id_t pid;
  pid = bbos_thread_get_port_id(bbos_sched_identify_myself());
  return bbos_port_fetch_message(pid);
}

bbos_message_t*
bbos_kernel_alloc_message()
{
  if (!bbos_kernel_messaging_pool)
    return NULL;
  return mempool_alloc(bbos_kernel_messaging_pool);
}

/*
 * Port functions.
 */

#ifdef BBOS_CONFIG_UNLIMIT_PORT_SIZE
void
__bbos_kernel_init_port(bbos_port_id_t pid, int16_t sz)
{
  bbos_kernel_get_port(pid).head = bbos_kernel_get_port(pid).tail = NULL;
  bbos_kernel_get_port(pid).counter = 0;
}
#else /* BBOS_CONFIG_UNLIMIT_PORT_SIZE */
void
bbos_kernel_init_port(bbos_port_id_t pid, int32_t sz, bbos_message_t** mp)
{
  bbos_validate_port_id(pid);
  bbos_port_set_message_pool(pid, mp);
  bbos_kernel_ports[pid].head = 0;
  bbos_kernel_ports[pid].tail = 0;
  bbos_kernel_ports[pid].counter = 0;
  bbos_kernel_ports[pid].size = sz;
}
#endif /* BBOS_CONFIG_UNLIMIT_PORT_SIZE */

bbos_code_t
bbos_port_push_message(bbos_port_id_t pid, bbos_message_t* message)
{
#ifdef BBOS_CONFIG_UNLIMIT_PORT_SIZE
  if (bbos_kernel_get_port(pid).tail == NULL)
    {
      bbos_kernel_get_port(pid).head = message;
      bbos_kernel_get_port(pid).tail = message;
      message->next = NULL;
      return BBOS_SUCCESS;
    }
  message->next = bbos_kernel_get_port(pid).tail->next;
  bbos_kernel_get_port(pid).tail->next = message;
#else
  if (bbos_port_is_full(pid))
    {
      return BBOS_PORT_IS_FULL;
    }
  bbos_kernel_ports[pid].message_pool[bbos_kernel_ports[pid].tail] = message;
  bbos_kernel_ports[pid].tail = (int32_t)((bbos_kernel_ports[pid].tail + 1) % \
                                          bbos_kernel_get_port(pid).size);
  bbos_kernel_ports[pid].counter += 1;
#endif /* BBOS_CONFIG_UNLIMIT_PORT_SIZE */
  return BBOS_SUCCESS;
}

bbos_message_t*
bbos_port_fetch_message(bbos_port_id_t pid)
{
  bbos_message_t* msg;
#ifdef BBOS_CONFIG_UNLIMIT_PORT_SIZE
  if (bbos_kernel_get_port(pid).head == NULL)
    return NULL;
  msg = bbos_kernel_get_port(pid).head;
  if (bbos_kernel_get_port(pid).head == bbos_kernel_get_port(pid).tail)
    bbos_kernel_get_port(pid).tail = NULL;
  else
    bbos_kernel_get_port(pid).head = bbos_kernel_get_port(pid).head->next;
#else
  if (bbos_port_is_empty(pid))
    {
      return NULL;
    }
  msg = bbos_kernel_get_port(pid).message_pool[bbos_kernel_get_port(pid).head];
  bbos_kernel_ports[pid].head = (bbos_kernel_ports[pid].head + 1) % \
    bbos_kernel_ports[pid].size;
  bbos_kernel_get_port(pid).counter -= 1;
#endif /* BBOS_CONFIG_UNLIMIT_PORT_SIZE */
  return msg;
}

/*
 * Copyright (c) 2011 Sladeware LLC
 */

#include <bb/os/kernel.h>
#include <bb/mm/mempool.h>
#include <bb/os/delay.h>

#include <stdio.h>
#include <stddef.h>

void
t0()
{
  bbos_message_t* msg;
  if ((msg = bbos_alloc_message()) == NULL) {
    bbos_panic("Can not allocate memory for a message\n");
  }

  msg->command = PING;
  msg->data = NULL;
  bbos_send_message(T1, msg);
}

void
t1()
{
  bbos_message_t* msg;

  if (bbos_receive_message(&msg) != BBOS_SUCCESS) {
    return; /* wait for a message */
  }
  
  switch (msg->command) {
  case PING:
    printf("Ping from %d\n", msg->sender);
    break;
  }
  
  bbos_free_message(msg);
  
  /* A delay in second, so we humans can see what is happening... */
  bbos_delay_sec(1);
}

int
main()
{
  bbos_init();
  PRIVATE BBOS_MEMPOOL(mp, 10, sizeof(bbos_message_t));
  bbos_mempool_init(mp, 10, sizeof(bbos_message_t));
  bbos_add_thread(T0, t0, mp);
  bbos_add_thread(T1, t1, NULL);
  return bbos_start();
}


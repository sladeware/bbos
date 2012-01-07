/*
 * Copyright (c) 2012 Sladeware LLC
 */

#include <bb/os.h>
#include <bb/os/kernel/time.h>
#include <bb/mm/mempool.h>

#define BBOS_PORT_MESSAGE_POOL(name, sz) \
  bbos_message_t* name[sz * sizeof(bbos_message_t*)]

#ifndef BBOS_CONFIG_UNLIMIT_PORT_SIZE
  BBOS_PORT_MESSAGE_POOL(msgpool0, 5);
  BBOS_PORT_MESSAGE_POOL(msgpool1, 5);
#endif

void
thread0_runner()
{
  bbos_message_t* msg;
  printf("> THREAD0 is running\n");
  msg = bbos_kernel_alloc_message();
  if (!msg)
    {
      printf("Cannot allocate message. Stand by and waiting...\n");
      return;
    }
  msg->command = PING;
  printf("Sending message '%p' with command '%d' to port '%d'... ",
         msg,
         PING,
         THREAD1);
  if (bbos_kernel_send_message(msg, PORT1) == BBOS_SUCCESS)
    printf("SUCCESS\n");
  else
    printf("FAILURE\n");
  bbos_delay_sec(1);
}

void
thread1_runner()
{
  bbos_message_t* msg;
  printf("> THREAD1 is running ***\n");
  msg = bbos_kernel_receive_message();
  if (!msg)
    {
      printf("No new messages\n");
      return;
    }
  printf("A new message received: %p\n", msg);
  printf("\towner   : %d\n", bbos_message_get_owner(msg));
  printf("\tcommand : %d\n", bbos_message_get_command(msg));
  bbos_delay_sec(1);
}

void
main()
{
  bbos();
  bbos_kernel_init_port(PORT0, 5, msgpool0);
  bbos_kernel_init_port(PORT1, 5, msgpool1);
  bbos_kernel_init_thread(THREAD0, thread0_runner, PORT0);
  bbos_kernel_init_thread(THREAD1, thread1_runner, PORT1);
  bbos_kernel_enable_all_threads();
  bbos_kernel_start();
}

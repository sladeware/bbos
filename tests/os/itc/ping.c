/*
 * This test runs a bunch of threads that communicate with each other.
 * Each thread tries to ping all other buddies one by one. However it
 * can only process one message or send it at one iteration.
 *
 * Copyright (c) 2012 Sladeware LLC
 */

#include <bb/os.h>
#include <bb/os/kernel/time.h>
#include <bb/mm/mempool.h>

#define BBOS_PORT_MESSAGE_POOL(name, sz) \
  bbos_message_t* name[sz * sizeof(bbos_message_t*)]

//#ifndef BBOS_CONFIG_UNLIMIT_PORT_SIZE
  BBOS_PORT_MESSAGE_POOL(msgpool0, 5);
  BBOS_PORT_MESSAGE_POOL(msgpool1, 5);
  BBOS_PORT_MESSAGE_POOL(msgpool2, 5);
  BBOS_PORT_MESSAGE_POOL(msgpool3, 5);
  BBOS_PORT_MESSAGE_POOL(msgpool4, 5);
  BBOS_PORT_MESSAGE_POOL(msgpool5, 5);
  BBOS_PORT_MESSAGE_POOL(msgpool6, 5);
//#endif

static bbos_thread_id_t done = BBOS_CONFIG_NR_THREADS;
static bbos_thread_id_t ping_me[BBOS_CONFIG_NR_THREADS];

/* Each thread runs main ping primitive in order to ping another
   thread. */
static void
ping(bbos_thread_id_t tid)
{
  bbos_message_t* msg;

  /* Define whether we have a new ping message from buddies. */
  if ((msg = bbos_kernel_receive_message()) != NULL)
    {
      printf("Received a new message <%p> with command '%d' from '%d'\n",
             msg, bbos_message_get_owner(msg), bbos_message_get_command(msg));
      return;
    }

  if (!ping_me[tid])
    {
      printf("All threads was pinged.\n");
      if (!done--)
        {
          bbos_kernel_stop();
        }
      return;
    }
  msg = bbos_kernel_alloc_message();
  if (!msg)
    {
      printf("Cannot allocate message. Stand by and waiting...\n");
      return;
    }
  msg->command = PING;
  printf("Sending message <%p> with command '%d' to port '%d'... ",
         msg, PING, ping_me[tid]);
  if (bbos_kernel_send_message(msg, ping_me[tid]) == BBOS_SUCCESS)
    {
      printf("SUCCESS\n");
      ping_me[tid]--;
    }
  else
    printf("FAILURE\n");
}

/* A small delay, so we humans can see what is happinig. */
#define PING_THREAD(tid)                            \
  static void                                       \
  thread ## tid ## _runner()                        \
  {                                                 \
    printf(">>> THREAD" #tid " is running\n");      \
    ping(tid);                                      \
    bbos_delay_sec(1);                              \
  }

PING_THREAD(0);
PING_THREAD(1);
PING_THREAD(2);
PING_THREAD(3);
PING_THREAD(4);
PING_THREAD(5);
PING_THREAD(6);

void
main()
{
  bbos_thread_id_t tid;

  bbos();
  bbos_kernel_init_port(PORT0, 5, msgpool0);
  bbos_kernel_init_port(PORT1, 5, msgpool1);
  bbos_kernel_init_port(PORT2, 5, msgpool2);
  bbos_kernel_init_port(PORT3, 5, msgpool3);
  bbos_kernel_init_port(PORT4, 5, msgpool4);
  bbos_kernel_init_port(PORT5, 5, msgpool5);
  bbos_kernel_init_port(PORT6, 5, msgpool6);
  /* Application threads */
  for (tid = 0; tid < BBOS_CONFIG_NR_THREADS; tid++)
    {
      ping_me[tid] = BBOS_CONFIG_NR_THREADS - 1;
    }
  bbos_kernel_init_thread(THREAD0, thread0_runner, PORT0);
  bbos_kernel_init_thread(THREAD1, thread1_runner, PORT1);
  bbos_kernel_init_thread(THREAD2, thread2_runner, PORT2);
  bbos_kernel_init_thread(THREAD3, thread3_runner, PORT3);
  bbos_kernel_init_thread(THREAD4, thread4_runner, PORT4);
  bbos_kernel_init_thread(THREAD5, thread5_runner, PORT5);
  bbos_kernel_init_thread(THREAD6, thread6_runner, PORT6);
  bbos_kernel_enable_all_threads();
  bbos_kernel_start();
}

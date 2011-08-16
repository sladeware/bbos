/*
 * Copyright (c) 2011 Sladeware LLC
 */

#include <stdio.h>

#include <bb/os/kernel.h>

static bbos_thread_t bbos_thread_table[BBOS_NUM_THREADS];
static bbos_port_t bbos_port_table[BBOS_NUM_THREADS];

/**
 * Defines whether the port is empty. If the port is not empty, returns number
 * of messages inside.
 *
 * @param tid Thread identifier.
 *
 * @return
 *
 * Number of messages.
 */
bbos_message_number_t
bbos_port_is_empty(bbos_thread_id_t tid)
{
  return bbos_port_table[tid].count;
}

/**
 * Basic primitive for sending. Send message to the thread's port.
 *
 * @param receiver Receiver's thread identifier.
 * @param message Pointer to the message.
 * @param owner Owner's thread identifier.
 *
 * @return
 *
 * Kernel error code.
 */
bbos_error_t
bbos_port_send(bbos_thread_id_t receiver, bbos_message_t *message,
               bbos_thread_id_t owner)
{
  if (bbos_port_table[receiver].tail == NULL)
    {
      bbos_port_table[receiver].head = message;
      bbos_port_table[receiver].tail = message;
      message->next = NULL;
      return BBOS_SUCCESS;
    }

  message->next = bbos_port_table[receiver].tail->next;
  bbos_port_table[receiver].tail->next = message;

  message->owner = owner;

  return BBOS_SUCCESS;
}

/**
 * Basic primitive for receiving. Receive a message from the thread's port.
 *
 * @param tid Thread identifier.
 * @param message Pointer to the message.
 *
 * @return
 *
 * Kernel error code.
 */
bbos_error_t
bbos_port_receive(bbos_thread_id_t tid,
                  bbos_message_t *message)
{
  if (bbos_port_table[tid].head == NULL)
    return BBOS_FAILURE;

  *message = *bbos_port_table[tid].head;

  if (bbos_port_table[tid].head == bbos_port_table[tid].tail)
    bbos_port_table[tid].tail = NULL;
  else
    bbos_port_table[tid].head = bbos_port_table[tid].head->next;

  return BBOS_SUCCESS;
}

/**
 * Flush the port.
 *
 * @param tid Thread identifier.
 */
void
bbos_port_flush(bbos_thread_id_t tid)
{
  bbos_port_table[tid].head = bbos_port_table[tid].tail = NULL;
  bbos_port_table[tid].count = 0;
}

/**
 * Initialize a thread.
 */
void
bbos_thread_init(bbos_thread_id_t tid, void (*thread)(void))
{
  bbos_thread_table[tid] = thread;
}

/**
 * Run a thread.
 */
void
bbos_thread_run(bbos_thread_id_t tid)
{
  assert(bbos_thread_table[tid] != NULL);
  (*bbos_thread_table[tid])();
}

/**
 * Halt the system. Display a message, then perfom cleanups with exit.
 *
 * @param fmt The text string to print.
 *
 * @return
 *
 * The function should never return.
 */
void
bbos_panic(const char *fmt, ...)
{
#ifdef BBOS_DEBUG
  static char buf[128];
  va_list args;
  va_start(args, fmt);
  //vsnprintf(buf, sizeof(buf), fmt, args);
  va_end(args);
  printf("Panic: %s\n", buf);
#endif
  //exit(0);
}

#ifdef BBOS_SCHED_ENABLED
/**
 * Switch to the next thread.
 */
void
bbos_switch_thread()
{
  assert(bbos_sched_myself() < BBOS_NUMTHREADS);
  bbos_thread_run( bbos_sched_myself() );
}
#endif

/**
 * Start the thread and schedule it. Wrapper for bbos_thread_init() and
 * bbos_sched_enqueue().
 *
 * @param tid Thread identifier.
 * @param thread Pointer to the thread.
 *
 * @return
 *
 * Kernel error code.
 */
bbos_error_t
bbos_add_thread(bbos_thread_id_t tid, void (*thread)(void))
{
  assert(tid < BBOS_NUM_THREADS);
  bbos_thread_init(tid, thread);
#ifdef BBOS_SCHED_ENABLED
  bbos_sched_enqueue(tid);
#endif
  return BBOS_SUCCESS;
}

/**
 * Stop the thread and dequeue it from schedule. Wrapper for bbos_thread_init()
 * and bbos_sched_dequeue().
 *
 * @param tid Thread identifier.
 *
 * @return
 *
 * Kernel error code.
 */
bbos_error_t
bbos_remove_thread(bbos_thread_id_t tid)
{
  assert(tid < BBOS_NUM_THREADS);
  bbos_thread_init(tid, NULL);
#ifdef BBOS_SCHED_ENABLED
  bbos_sched_dequeue(tid);
#endif
  return BBOS_SUCCESS;
}

/**
 * The first function that you must call, while will initialize the kernel.
 *
 * @note
 *
 * A requirement of BBOS is that you call bbos_init() before you invoke
 * any of its other services.
 */
void
bbos_init()
{
  bbos_thread_id_t tid;

  printf(bbos_banner);

#ifdef BBOS_DEBUG
  printf("Initialize BBOS kernel\n");
#endif

  for (tid=0; tid<BBOS_NUM_THREADS; tid++)
    bbos_thread_init(tid, NULL);

#ifdef BBOS_SCHED_ENABLED
  bbos_sched_init();
#else
  printf("Scheduler was not enabled\n");
#endif
}

/**
 * Start the kernel.
 *
 * @return
 *
 * Kernel error code.
 */
bbos_error_t
bbos_start()
{
#ifdef BBOS_DEBUG
  printf("Start BBOS kernel\n");
#endif

#ifdef BBOS_SCHED_ENABLED
  bbos_add_thread(BBOS_IDLE, bbos_idle_runner);

  while (1) {
    bbos_sched_move();
    bbos_switch_thread();
  }
#else
  bbos_switch_thread();
#endif

  return BBOS_SUCCESS;
}

/**
 * Runs when the system is idle.
 */
void
bbos_idle_runner()
{
}

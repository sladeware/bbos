/*
 * Copyright (c) 2011 Sladeware LLC
 */

#include <stdio.h>
#include <bb/os/kernel.h>

static bbos_thread_t bbos_thread_table[BBOS_NR_THREADS];

/**
 * Defines whether the port is empty. If the port is not empty, returns number
 * of messages inside.
 *
 * @param tid Thread identifier.
 * @return Number of messages.
 */
bbos_message_number_t
bbos_port_is_empty(bbos_thread_id_t tid)
{
  return bbos_port_table[tid].count;
}

/**
 * Allocate memory for a new message.
 */
bbos_message_t*
bbos_alloc_message()
{
	return NULL;
}

/**
 * @brief Basic primitive for sending. Send message to the thread.
 * @param message Pointer to the message.
 * @param receiver Receiver's thread identifier.
 * @return Kernel error code.
 */
bbos_error_t
bbos_send_message(bbos_thread_id_t receiver, bbos_message_t* message)
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

  message->sender = 0;

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
 * @brief Initialize a thread.
 * @param tid Thread identifier
 * @param target Callable function to be invoked by the bbos_thread_start()
 */
void
bbos_thread_init(bbos_thread_id_t tid, bbos_thread_target_t target)
{
  bbos_thread_table[tid].target = target;
}

/**
 * @brief Start the thread's activity.
 * @param tid Thread identifier
 */
void
bbos_thread_start(bbos_thread_id_t tid)
{
  assert(bbos_thread_table[tid] != NULL);
  (*bbos_thread_table[tid].target)();
}

#ifdef BBOS_SCHED_ENABLED

/**
 * @brief Switch to the next thread.
 * @see bbos_thread_start()
 */
static void
bbos_switch_thread()
{
  assert(bbos_sched_get_running_thread() < BBOS_NR_THREADS);
  bbos_thread_start( bbos_sched_get_running_thread() );
}

#endif

/**
 * @brief Start the thread and schedule it. Wrapper for bbos_thread_init() and
 * bbos_sched_enqueue_thread() functions.
 * @param tid Thread identifier.
 * @param thread Pointer to the thread.
 * @return Kernel error code.
 * @see bbos_thread_init()
 * @see bbos_sched_enqueue_thread()
 */
bbos_error_t
bbos_add_thread(bbos_thread_id_t tid, void (*target)(void))
{
  bbos_thread_init(tid, target);
#ifdef BBOS_SCHED_ENABLED /* scheduler thread if possible */
  bbos_sched_enqueue(tid);
#endif
  return BBOS_SUCCESS;
}

/**
 * @brief Stop the thread and dequeue it from schedule. Wrapper for
 * bbos_thread_init() and bbos_sched_dequeue_thread() functions.
 * @param tid Thread identifier
 * @return Kernel error code.
 * @see bbos_thread_init()
 * @see bbos_sched_dequeue_thread()
 */
bbos_error_t
bbos_remove_thread(bbos_thread_id_t tid)
{
  bbos_thread_init(tid, NULL);
#ifdef BBOS_SCHED_ENABLED /* remove from scheduler if possible */
  bbos_sched_dequeue_thread(tid);
#endif
  return BBOS_SUCCESS;
}

/**
 * @brief Halt the system. Display a message, then perfom cleanups with exit.
 * @param fmt The text string to print.
 * @return The function should never return.
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

/**
 * @brief Print debug information. Produce zero code unless BBOS_DEBUG is 
 * defined.
 */
#ifdef defined(BBOS_DEBUG)
#define bbos_print_debug(fmt, ...) printf(fmt, ##__VA_ARGS__)
#else
#define bbos_print_debug(fmt, ...) 0
#endif

/**
 * @brief The first function that you must call, while will initialize the 
 * kernel.
 * @note A requirement of BBOS is that you call bbos_init() before you invoke
 * any of its other services.
 * @see bbos_sched_init()
 */
void
bbos_init()
{
  bbos_thread_id_t tid;

  bbos_print_debug(bbos_banner);
  bbos_print_debug("Initialize BBOS kernel\n");

  /* Initialize threads one by one */
  for (tid = 0; tid < BBOS_NR_THREADS; tid++) {
    bbos_thread_init(tid, NULL);
  }

  /* Initialize scheduler if it was enabled */
#ifdef BBOS_SCHED_ENABLED
  bbos_sched_init();
#else
  bbos_print_debug("Scheduler was not enabled\n");
#endif
}

/**
 * @brief Start the kernel
 * @return Kernel error code.
 * @see bbos_sched_move()
 * @see bbos_switch_thread()
 */
bbos_error_t
bbos_start()
{
  bbos_print_debug("Start BBOS kernel\n");

#ifdef BBOS_SCHED_ENABLED
  /* Add idle thread to trace whether system is idle or not */
  bbos_add_thread(BBOS_IDLE, bbos_idle);

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
 * @brief This thread runs when the system is idle.
 */
void
bbos_idle()
{
}


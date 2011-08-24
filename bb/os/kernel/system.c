/*
 * Copyright (c) 2011 Sladeware LLC
 */

#include <stdio.h>
#include <stdlib.h>

#include <bb/os/kernel.h>
#include <bb/mm/mempool.h>

PUBLIC bbos_thread_t bbos_thread_table[BBOS_NR_THREADS];

/**
 * Allocate memory for a new message. This function is provided to escape
 * from the standard @c bbos_alloc() memory allocator. It's up to running thread
 * to manage memory allocation for a message-passing. Therefore the memory will
 * be taken from a special memory pool from a tread context.
 * @return Pointer to the message structure.
 * @see bbos_free_message()
 */
bbos_message_t*
bbos_alloc_message()
{
  void** message;
  BBOS_MEMPOOL_ALLOC(&bbos_get_running_thread().mp, message);
  return (bbos_message_t*)message;
}

/**
 * Free memory used by a message. This function is provided in order to escape
 * from the standard @c bbos_free(). The very important to keep right thread
 * identifier in @c sender field. By using this field the memory will be
 * returned to its owner.
 * @param message Pointer to the message.
 * @see bbos_alloc_message()
 */
void
bbos_free_message(bbos_message_t* message)
{
  BBOS_MEMPOOL_FREE(&bbos_thread_table[message->sender].mp, (void *)message);
}

/**
 * Basic primitive for message sending. Send message to @c receiver.
 * @param message Pointer to the message.
 * @param receiver Receiver's thread identifier.
 * @note The message has to be previously allocated will help of
 * bbos_alloc_message() function.
 * @return Kernel error code.
 * @see bbos_alloc_message()
 */
bbos_error_t
bbos_send_message(bbos_thread_id_t receiver, bbos_message_t* message)
{
  return BBOS_SUCCESS;
}

/**
 * Basic primitive for receiving. Receive a message for currently running
 * thread.
 *
 * @param message Pointer to the pointer where the message has to be stored
 * @return Kernel error code.
 */
bbos_error_t
bbos_receive_message(bbos_message_t **message)
{
  return BBOS_SUCCESS;
}

/**
 * @brief Initialize a thread.
 * @param tid Thread identifier
 * @param target Callable function to be invoked by the bbos_thread_start()
 * @param mp Pointer to the memory pool for messages
 */
void
bbos_thread_init(bbos_thread_id_t tid, bbos_thread_target_t target, void* mp)
{
  bbos_thread_table[tid].target = target;
  bbos_thread_table[tid].mp = mp;
}

/**
 * @brief Start the thread's activity.
 * @param tid Thread identifier
 */
void
bbos_thread_start(bbos_thread_id_t tid)
{
  assert(bbos_thread_table[tid].target != NULL);
  (*bbos_thread_table[tid].target)();
}

/**
 * @brief Start the thread and schedule it. Wrapper for bbos_thread_init() and
 * bbos_sched_enqueue_thread() functions.
 * @param tid Thread identifier.
 * @param thread Pointer to the thread.
 * @return Kernel error code.
 * @see bbos_thread_init()
 * @see bbos_sched_enqueue()
 */
bbos_error_t
bbos_add_thread(bbos_thread_id_t tid, void (* target)(void), void* mp)
{
  bbos_thread_init(tid, target, mp);
  bbos_sched_enqueue(tid); /* scheduler thread if possible */
  return BBOS_SUCCESS;
}

/**
 * @brief Stop the thread and dequeue it from schedule. Wrapper for
 * bbos_thread_init() and bbos_sched_dequeue() functions.
 * @param tid Thread identifier
 * @return Kernel error code.
 * @see bbos_thread_init()
 * @see bbos_sched_dequeue()
 */
bbos_error_t
bbos_remove_thread(bbos_thread_id_t tid)
{
  bbos_thread_init(tid, NULL, NULL);
  bbos_sched_dequeue(tid); /* remove from schedule if possible */
  return BBOS_SUCCESS;
}

/**
 * @brief This thread runs when the system is idle.
 */
void
bbos_idle()
{
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
  vsnprintf(buf, sizeof(buf), fmt, args);
  va_end(args);
  printf("Panic: %s\n", buf);
#endif
  exit(0);
}

/**
 * @brief Print debug information. Produce zero code unless BBOS_DEBUG is
 * defined.
 */
#if defined(BBOS_DEBUG)
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
    bbos_thread_init(tid, NULL, NULL);
  }

  /* Initialize scheduler if it was enabled */
  bbos_print_debug("Initialize scheduler \"" BBOS_SCHED_STR "\"\n");
  bbos_sched_init();
}

#ifndef bbos_loop
/**
 * BBOS main loop.
 */
static void
bbos_loop()
{
  while (TRUE) {
    bbos_sched_move();
    bbos_switch_thread();
  }
}
#endif /* bbos_loop */

/**
 * @brief Start the kernel
 * @return Kernel error code.
 * @see bbos_lopp()
 */
bbos_error_t
bbos_start()
{
  bbos_print_debug("Start BBOS kernel\n");

#ifdef BBOS_SCHED_ENABLED
  ///* Add idle thread to trace whether system is idle or not */
  //bbos_add_thread(BBOS_IDLE, bbos_idle);
#endif

  bbos_loop();

  return BBOS_SUCCESS;
}

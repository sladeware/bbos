#ifndef __BB_OS_TYPES_H
#define __BB_OS_TYPES_H

/*
 * TODO: generate port id at buildtime
 */
#ifndef bbos_port_id_t
typedef uint8_t bbos_port_id_t;
#endif

/**
 * Buildtime defined type for thread identifier. By default represents up to 255
 * threads.
 */
#ifndef bbos_thread_id_t
typedef uint8_t bbos_thread_id_t;
#endif

/**
 * Thread execution data type.
 */
typedef void (*bbos_thread_runner_t)(void);

struct bbos_thread {
  bbos_thread_runner_t runner; /* Pointer to the target function to be called.*/
};

typedef void* mempool;

#ifndef bbos_message_label_t
typedef uint8_t bbos_message_label_t;
#endif /* bbos_message_label_t */

/**
 * Message structure passed between threads.
 */
struct bbos_message {
  bbos_port_id_t receiver;
  bbos_port_id_t sender;
  bbos_message_label_t label; /* what kind of message is it */
  void* payload;
};

struct bbos_port {
  mempool pool;
  struct bbos_message** inbox;
  size_t capacity;
  size_t counter; /* count number of unread messages. */
};

#endif /* __BB_OS_TYPES_H */

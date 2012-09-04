#ifndef __BB_OS_THREAD_H
#define __BB_OS_THREAD_H

#include "port.h"

/* Thread identifier represents up to 255 threads. */
typedef uint8_t bbos_thread_id_t;

/* Thread execution data type. */
typedef void (*bbos_thread_runner_t)(void);

struct bbos_thread {
  bbos_thread_runner_t runner; /* Pointer to the target function to be called.*/
  struct bbos_port* default_port;
};
typedef struct bbos_thread bbos_thread_t;

#endif /* __BB_OS_THREAD_H */

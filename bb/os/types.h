/*
 * Copyright (c) 2011 Sladeware LLC
 */

#ifndef __BBOS_TYPES_H
#define __BBOS_TYPES_H

/**
 * @file bb/os/types.h
 * @brief Important OS data type definitions
 */

/**
 * BBOS error type.
 */
typedef int32_t bbos_error_t;

/**
 * Thread identifier. Represents up to 255 threads.
 */
typedef uint8_t bbos_thread_id_t;

/**
 * Thread execution data type.
 */
typedef void (*bbos_thread_target_t)(void);

struct bbos_thread {
  bbos_thread_target_t target; /**< Target */
  void* mp; /**< Pointer to the memory pool with messages */
};

/**
 * @typedef bbos_thread_t
 * @brief Thread running context
 */
typedef struct bbos_thread bbos_thread_t;

/**
 * An @c int type typically used to convey message type or operation id for the
 * receiver.
 */
typedef int bbos_message_command_t;

/**
 * @struct bbos_message
 * @brief BBOS message structure
 */
struct bbos_message {
  bbos_message_command_t command; /**< What kind of message is it. */
  bbos_thread_id_t sender; /**< Who sendes the message. */
  void *data; /**< Pointer to the message data. */
};

/**
 * Describe message structure.
 */
typedef struct bbos_message bbos_message_t;

#endif /* __BBOS_TYPES_H */

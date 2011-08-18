/*
 * Copyright (c) 2011 Sladeware LLC
 */
 
#ifndef __BBOS_TYPES_H
#define __BBOS_TYPES_H

/**
 * @file types.h
 * @brief Important data type definitions
 *
 * It is considered good programming practice to use these definitions, instead 
 * of the underlying base type. By convention, all type names have postfix 
 * @b _t.
 */

#include <limits.h>

#ifdef HAVE_INTTYPES_H
#include <inttypes.h>
#endif

#ifdef HAVE_STDINT_H
#include <stdint.h>
#endif

#ifdef HAVE_STDDEF_H
#include <stddef.h>
#endif

#ifndef _SIZE_T
#define _SIZE_T
/**
 * The type size_t holds all results of the sizeof operator.  At first glance,
 * it seems obvious that it should be an unsigned int, but this is not always 
 * the case. 
 */
typedef unsigned int size_t;
#endif

#ifndef _SSIZE_T
#define _SSIZE_T
/** The type ssize_t is the signed version of size_t. */
typedef int ssize_t;
#endif

/** Represents signed integers with values ranging from -128 to 127. */
typedef char int8_t;

/** Represents unsigned integers with values ranging from 0 to 255. */
typedef unsigned char uint8_t;

/** Represents signed integers with values ranging from -32,768 to 32,767. */
typedef signed short int16_t;

/** Represents unsigned integers with values ranging from 0 to 65,535. */
typedef unsigned short uint16_t;

/**
 * Represents signed integers with values ranging from −2,147,483,648 to 
 * 2,147,483,647.
 */
typedef signed int int32_t;

/** Represents unsigned integers with values ranging from 0 to 4,294,967,295. */
typedef unsigned int uint32_t;

/** 
 * Represents unsigned integers with values ranging from 0 to 
 * 18,446,744,073,709,551,615.
 */
typedef long long uint64_t;

/** Boolena type with values TRUE and FALSE. */
typedef unsigned char bool_t;

/** BBOS error type. */
typedef int32_t bbos_error_t;

/** Thread identifier. Represents up to 255 threads. */
typedef uint8_t bbos_thread_id_t;

/** Thread execution data type. */
typedef void (*bbos_thread_t)(void);

/**
 * An int type typically used to convey message type or operation id for the 
 * receiver.
 */
typedef int bbos_message_id_t;

/** An size_t data type used to store the size of a message. */
typedef size_t bbos_message_size_t;

/** Message's sequence number in the port. Describes up to 65,535 messages. */
typedef uint16_t bbos_message_number_t;

/** Integer contant 0. Used for turning integers into booleans. */
#define FALSE 0

/** Integer constant @c !FALSE or 1. Used for turning integers into booleans. */
#define TRUE (!FALSE)

/**
 * @struct bbos_message
 * @brief BBOS message
 */
struct bbos_message {
  bbos_message_id_t id; /**< What kind of message is it. */
  bbos_thread_id_t owner; /**< Who owns the message. */
  void *data; /**< Pointer to the message data. */
  bbos_message_size_t size; /**< The message's size. */
  struct bbos_message *next; /**< Pointer to the next message in the queue.*/
};

/** Describe message structure. */
typedef struct bbos_message bbos_message_t;

/** 
 * @struct bbos_port
 * @brief Queue of messages for particular thread
 */
struct bbos_port {
  bbos_message_t *head; /**< Pointer to the first message in the list. */
  bbos_message_t *tail; /**< Pointer to the last message in the list. */
  uint16_t count; /**< Count of pending messages. */
};

typedef struct bbos_port bbos_port_t;

#endif


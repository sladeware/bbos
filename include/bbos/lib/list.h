/*
 * List data structure.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_LIB_LIST_H
#define __BBOS_LIB_LIST_H

#include <bbos/env.h>
#include <bbos/lib/memory/fastmempool.h>

struct list_node {
  void *data;
  struct list_node *next;
};

typedef struct list_node list_node_t;
typedef list_node_t * list_link_t;

struct list {
  int16_t size;
  int16_t counter;
  list_node_t* head;
  list_node_t* tail;	
  fastmempool_t *mempool;
};

typedef struct list list_t;

/* List overhead */
enum {
  LIST_OVERHEAD = ((size_t)sizeof(list_t))
};

#define LIST_PARTITION_SIZE(n)						\
  (sizeof(list_t) + FASTMEMPOOL_PARTITION_SIZE(n, sizeof(void *)))

#define LIST_PARTITION(name, n)			\
  int8_t name[LIST_PARTITION_SIZE(n)]

#define list_counter(list) ((list)->counter)

#define list_size(list) ((list)->size)

#define list_head(list) ((list)->head)

#define list_tail(list) ((list)->tail)

#define list_data(node) ((node)->data)

#define list_next(node) ((node)->next)

/**
 * LIST_FOR_EACH - Iterate over a list.
 * @node: Pointer to the node for your list.
 * @head: Pointer to the head for your list.
 */
#define LIST_FOR_EACH(node, head)				\
  for (node = (head); node != NULL; node = node->next)

list_t *list_init(int8_t *part, int16_t sz);

bbos_return_t list_insert(list_t *list, list_node_t *node, const void *data); 

void *list_remove(list_t *list, list_node_t *node);

#endif /* __BBOS_LIB_LIST_H */

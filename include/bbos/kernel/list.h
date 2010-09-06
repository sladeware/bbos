/*
 * List data structure.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_LIST_H
#define __BBOS_LIST_H

#ifdef __cplusplus
extern "C" {
#endif

struct bbos_list_node {
  void *data;
  struct bbos_list_node *next;
};

typedef struct bbos_list_node bbos_list_node_t;
typedef bbos_list_node_t *bbos_list_link_t;

struct bbos_list {
  int16_t size;
  int16_t counter;
  bbos_list_node_t* head;
  bbos_list_node_t* tail;
  bbos_mempool_t *mempool;
};

typedef struct bbos_list bbos_list_t;

/* List overhead */
enum {
  BBOS_LIST_OVERHEAD = ((size_t)sizeof(bbos_list_t))
};

#define BBOS_LIST_PARTITION_SIZE(n)						\
  (sizeof(bbos_list_t) + BBOS_MEMPOOL_PARTITION_SIZE(n, sizeof(void *)))

#define BBOS_LIST_PARTITION(name, n)			\
  int8_t name[BBOS_LIST_PARTITION_SIZE(n)]

#define bbos_list_counter(list) ((list)->counter)

#define bbos_list_size(list) ((list)->size)

#define bbos_list_head(list) ((list)->head)

#define bbos_list_tail(list) ((list)->tail)

#define bbos_list_data(node) ((node)->data)

#define bbos_list_next(node) ((node)->next)

/**
 * BBOS_LIST_FOR_EACH - Iterate over a list.
 * @node: Pointer to the node for your list.
 * @head: Pointer to the head for your list.
 */
#define BBOS_LIST_FOR_EACH(node, head)				\
  for (node = (head); node != NULL; node = node->next)

/* Prototypes */

bbos_list_t *bbos_list_create(int8_t *part, int16_t sz);

bbos_return_t bbos_list_insert(bbos_list_t *list, bbos_list_node_t *node,
	const void *data);

void *bbos_list_remove(bbos_list_t *list, bbos_list_node_t *node);

void bbos_list_destroy(struct bbos_list *list);

#ifdef __cplusplus
}
#endif

#endif /* __BBOS_LIST_H */


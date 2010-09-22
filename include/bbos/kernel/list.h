/*
 * List data structure.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_KERNEL_LIST_H
#define __BBOS_KERNEL_LIST_H

#ifdef __cplusplus
extern "C" {
#endif

struct bbos_list_node {
  void *data;
  struct bbos_list_node *next;
};

struct bbos_list {
  int16_t size;
  int16_t counter;
  struct bbos_mempool *pool;
  struct bbos_list_node* head;
  struct bbos_list_node* tail;
};

typedef struct bbos_list_node bbos_list_node_t;
typedef bbos_list_node_t *bbos_list_link_t;
typedef struct bbos_list bbos_list_t;

#define BBOS_LIST_PARTITION_SIZE(n)			\
  (n * sizeof(struct bbos_list_node))

#define BBOS_LIST_PARTITION(name, n)		\
  int8_t name[BBOS_LIST_PARTITION_SIZE(n)]

#define bbos_list_counter(list) ((list)->counter)

#define bbos_list_size(list) ((list)->size)

#define bbos_list_head(list) ((list)->head)

#define bbos_list_tail(list) ((list)->tail)

#define bbos_list_data(node) ((node)->data)

#define bbos_list_next(node) ((node)->next)

#define bbos_list_insert_head(list, data) \
  bbos_list_insert(list, bbos_list_tail(list), data)

/**
 * BBOS_LIST_FOR_EACH - Iterate over a list.
 * @node: Pointer to the node for your list.
 * @head: Pointer to the head for your list.
 */
#define BBOS_LIST_FOR_EACH(node, head)			\
  for (node = (head); node != NULL; node = node->next)

/* Prototypes */

bbos_return_t bbos_list_init(struct bbos_list *list, int8_t *part, int16_t n);

bbos_return_t bbos_list_insert(struct bbos_list *list, 
  struct bbos_list_node *node, const void *data);

void *bbos_list_remove(struct bbos_list *list, struct bbos_list_node *node);

void bbos_list_destroy(struct bbos_list *list);

#ifdef __cplusplus
}
#endif

#endif /* __BBOS_KERNEL_LIST_H */


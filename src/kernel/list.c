/*
 * List data structure.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#include <bbos.h>

/**
 * bbos_list_create - Create the linked list.
 * @part: Pointer to the memory partition.
 * @sz: Number of nodes in the list.
 *
 * Return value:
 *
 * Pointer to list.
 *
 * Complexity:
 *
 * O(n), where n is the number of nodes in the list.
 */
bbos_list_t *
bbos_list_create(int8_t *part, int16_t sz)
{
  bbos_list_t *list;

  assert(part);
	assert(sz > 0);

  list = (bbos_list_t *)part;
  list->mempool = bbos_mempool_create(part + BBOS_LIST_OVERHEAD, sz,
		sizeof(bbos_list_node_t));

  list->size = sz;
  list->counter = 0;
  list->head = NULL;
  list->tail = NULL;

  return list;
}

/**
 * bbos_list_insert - Inserts an nodes just after node in the linked list.
 * @list: Pointer to the list.
 * @node: Pointer to the specified node.
 * @data: Pointer to the data to be stored.
 *
 * Return value:
 *
 * BBOS_SUCCESS if inserting the node is successful, or BBOS_FAILURE otherwise.
 *
 * Complexity:
 *
 * O(1)
 */
bbos_return_t
bbos_list_insert(bbos_list_t *list, bbos_list_node_t *node, const void *data)
{
  bbos_list_node_t *new_node;

  /*
   * Allocate storage for the node.
   * Do not need to check the counter. Use fastmempool instead.
   */
  if ((new_node = (bbos_list_node_t *)bbos_mempool_alloc(list->mempool)) == NULL) {
    return BBOS_FAILURE;
  }

  /* Insert the node into the list. */
  new_node->data = (void *)data;

  if (node == NULL) {
    /* Handle insertion at the head of the list. */

    if (bbos_list_counter(list) == 0) {
      list->tail = new_node;
    }

    new_node->next = list->head;
    list->head = new_node;
  }
  else {
    /* Handle insertion somewhere other than at the head. */

    if (node->next == NULL) {
      list->tail = new_node;
    }

    new_node->next = node->next;
    node->next = new_node;
  }

  /* Adjust the size of the list to account for the inserted node. */
  list->counter++;

  return BBOS_SUCCESS;
}

/**
 * bbos_list_remove - Removes the node just after the specified node from the
 * linked list.
 * @list: Pointer to the list.
 * @node: Pointer to the specified node.
 * @data: Pointer to the data.
 *
 * Return value:
 *
 * Pointer to the removed data, or NULL otherwise.
 *
 * Complexity:
 *
 * O(1)
 *
 * TODO:
 *
 * Pointer to an error can be added as an argument.
 */
void *
bbos_list_remove(bbos_list_t *list, bbos_list_node_t *node)
{
  void *data;
  bbos_list_node_t *old_node;

  /* Do not allow removal from an empty list */
  if (bbos_list_counter(list) == 0) {
    return (void *)NULL;
  }

  /* Remove the node from the list. */
  if (node == NULL) {
    /* Handle removal from the head of the list. */
    data = list->head->data;
    old_node = list->head;
    list->head = list->head->next;

    if (bbos_list_counter(list) == 1) {
      list->tail = NULL;
    }
  }
  else {
    /* Handle removal from somewhere other than the head. */
    if (node->next == NULL) {
      return (void *)NULL;
    }

    data = node->next->data;
    old_node = node->next;
    node->next = node->next->next;

    if (node->next == NULL) {
      list->tail = node;
    }
  }

  bbos_mempool_free(list->mempool, old_node);

  /* Adjust the size of the list to account for the removed node. */
  list->counter--;

  return data;
}

/**
 * bbos_list_destroy - Destroy the list.
 * @list: Pointer to the list.
 */
void
bbos_list_destroy(struct bbos_list *list)
{
	bbos_mempool_destroy(list->mempool);
}


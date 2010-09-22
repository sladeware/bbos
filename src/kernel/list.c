/*
 * List data structure.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#include <bbos.h>

/**
 * bbos_list_init - Initialize linked list.
 * @list: Pointer to the list structure.
 * @part: Pointer to the memory partition.
 * @n: Number of nodes in the list.
 *
 * Return value:
 *
 * Generic code.
 *
 * Complexity:
 *
 * O(n), where n is the number of nodes in the list.
 */
bbos_return_t
bbos_list_init(struct bbos_list *list, int8_t *part, int16_t n)
{
  assert(part);
  assert(n > 0);

  bbos_mempool_init(list->pool, part, n, sizeof(struct bbos_list_node));

  list->size = n;
  list->counter = 0;
  list->head = list->tail = NULL;

  return BBOS_SUCCESS;
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
bbos_list_insert(struct bbos_list *list, struct bbos_list_node *node, 
  const void *data)
{
  struct bbos_list_node *new_node;

  /*
   * Allocate storage for the node.
   * Do not need to check the counter. Use mempool instead.
   */
  if ((new_node = (struct bbos_list_node *)bbos_mempool_allocate(list->pool)) == NULL) {
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
bbos_list_remove(struct bbos_list *list, struct bbos_list_node *node)
{
  void *data;
  struct bbos_list_node *old_node;

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

  bbos_mempool_free(list->pool, old_node);

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
  bbos_mempool_destroy(list->pool);
}


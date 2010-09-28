
#ifndef __BBOS_MQUEUE_H
#define __BBOS_MQUEUE_H

struct bbos_mqueue {
  void **in;
  void **out;
  void **begin;
  void **end;
  size_t counter;
  size_t size;
};

bbos_return_t bbos_mqueue_init(struct bbos_mqueue *mq, void **part, 
  size_t size);

bbos_return_t bbos_mqueue_send(struct bbos_mqueue *mq, void *msg);

void *bbos_mqueue_receive(struct bbos_mqueue *mq);

bbos_return_t bbos_mqueue_destroy(struct bbos_mqueue *mq);

#endif /* __BBOS_MQUEUE_H */


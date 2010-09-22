
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

#endif /* __BBOS_MQUEUE_H */


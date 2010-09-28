
#include <bbos.h>

bbos_return_t
bbos_mqueue_init(struct bbos_mqueue *mq, void **part, size_t size)
{
  mq->begin = part;
  mq->end = &part[size];
  mq->in = mq->out = part;
  mq->size = size;
  mq->counter = 0;

  return BBOS_SUCCESS;
}


bbos_return_t
bbos_mqueue_send(struct bbos_mqueue *mq, void *msg)
{
  /* Make sure queue is not full */
  if(mq->counter >= mq->size) {
    return BBOS_FAILURE;
  }

  /* Insert message into queue and update the counter */
  *mq->in++ = msg;
  mq->counter++;

  if(mq->in == mq->end) {
    mq->in = mq->begin;
  }

  return BBOS_SUCCESS;
}

void *
bbos_mqueue_receive(struct bbos_mqueue *mq)
{
  void *msg;

  if(!mq->counter) {
    msg = *mq->out++;
    mq->counter--;

    if(mq->out == mq->end) {
      mq->out = mq->begin;
    }

    return msg;
  }

  return NULL;
}

bbos_return_t
bbos_mqueue_destroy(struct bbos_mqueue *mq)
{
}



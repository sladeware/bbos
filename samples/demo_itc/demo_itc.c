/*
 * This sample shows how to use ITC interface.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#include <stddef.h>
#include <stdio.h>
#include <string.h>
#include <bbos.h>
#include <bbos/lib/delay.h>

#define PORT0 0

BBOS_ITC_PORT(receiver_port0, 1, 10);

void receiver() {
  void* msg;

  printf("RECEIVER thread is running...\n");

  msg = bbos_itc_receive(PORT0);
  if (msg) {
    printf("RECEIVER has a new message: %s\n", msg);
    exit(0);
  }
  else {
    printf("Nothing to receive from the PORT0. Still waiting...\n");
  }
}

void sender() {
  void *msg;

  printf("SENDER thread is running...\n");

  /* Let us compose a new message */

  if ((msg = bbos_itc_compose(PORT0)) != NULL) {
    memcpy(msg, "Hello!\0", 7);
    printf("SENDER composed the message.\n");
    if(bbos_itc_send(msg) == BBOS_SUCCESS)
      printf("SENDER has sent the message: %s\n",msg);
    else
      printf("SENDER can not send the message.\n");
  } else
    printf("Can not compose a new message.\n");
}

bbos_return_t switcher(bbos_thread_id_t tid) {
  printf("Switch to thread %d\n", tid);

  switch(tid) {
  case RECEIVER_ID:
    receiver();
    break;
  case SENDER_ID:
    sender();
    break;
  case BBOS_IDLE_ID:
  	 break;
  default:
    return BBOS_FAILURE;
  }

  //sdelay(1);

  return BBOS_SUCCESS;
}

int main(void) {
  printf("ITC Demo!\n");

  bbos_init();

  /* Initialize ports */
  bbos_port_init(PORT0, receiver_port0, 1, 10);

  /* Start threads */
  bbos_thread_start(RECEIVER_ID);
  bbos_thread_start(SENDER_ID);

  bbos_start();

  return 0;
}


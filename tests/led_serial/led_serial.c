/*
 * Copyright (c) 2011 Sladeware LLC
 */

#include <bb/os/kernel.h>
#include BBOS_FIND_PROCESSOR_FILE(time.h)
#include <bb/os/drivers/serial/p8x32_uart/core.h>
#include <stdio.h>

void
receiver()
{
  int byte;
  static int init_complete = 0;

  if (!init_complete) {
    printf("Open serial\n");
    serial_open(31, 30, 0, 115200);
    init_complete = 1;
    return;
  }

  if (byte = serial_receive_byte()) {
    _dira(1<<byte, 1<<byte);
    _outa(1<<byte, 1<<byte);
    bbos_sleep_sec(2);
  }
}

int
main()
{
  bbos_init();
  bbos_add_thread(RECEIVER, receiver);
  return bbos_start();
}

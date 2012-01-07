/*
 * Copyright (c) 2012 Sladeware LLC
 */
#include <bb/os.h>
#include <stdio.h>

void
helloworld_runner()
{
  printf("Hello world!\n");
}

void
main()
{
  bbos();
  bbos_kernel_init_thread(HELLOWORLD, helloworld_runner, NULL);
  bbos_kernel_enable_thread(HELLOWORLD);
  bbos_kernel_start();
}



#include <stdio.h>
#include <bbos/kernel.h>

void helloworld()
{
  printf("Hello world!\n");
}

void main()
{
  bbos_init();
  bbos_start_thread(HELLOWORLD, helloworld);
  bbos_start();
}


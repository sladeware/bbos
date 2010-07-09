/*
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#include <lib/memory/bbos_mempool.h>

#define NUMBER_OF_BLOCKS 10
#define BLOCK_SIZE 100 // bytes

BBOS_MEMPOOL(testpool_buf, NUMBER_OF_BLOCKS, BLOCK_SIZE);

void
main()
{
  bbos_mempool_t* testpool;
  void* buf;

  testpool = bbos_mempool_init(testpool_buf, NUMBER_OF_BLOCKS, BLOCK_SIZE);
  buf = bbos_mempool_alloc(testpool);

  if(buf == NULL) {
    printf("Cannot allocate new memory block from the pool.\n");
    return;
  }

  memcpy(buf, "Hello world!\0", 13);

  printf("%s", buf);
}


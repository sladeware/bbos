/*
 * Copyright (c) 2013 Sladeware LLC
 */

#include <stdio.h>
#include "bb/os/mm/mempool.h"

MEMPOOL_PARTITION(port_part, 5, 20);

int
main()
{
  mempool port_pool;
  int i;
  void* blocks[5];
  port_pool = mempool_init(port_part, 5, 20);
  printf("Mempool: 0x%X\n", (int)port_pool);
  for (i = 0; i < 5; i++) {
    blocks[i] = mempool_alloc(port_pool);
    printf("Alloc block#%d: 0x%X\n", i, (int)blocks[i]);
  }
  // The next block is NULL-block
  printf("Alloc block#%d: 0x%X\n", i, (int)mempool_alloc(port_pool));
  for (i = 0; i < 5; i++) {
    printf("Free block#%d: 0x%X\n", i, (int)blocks[i]);
    mempool_free(port_pool, blocks[i]);
  }
  for (i = 0; i < 5; i++) {
    blocks[i] = mempool_alloc(port_pool);
    printf("Alloc block#%d: 0x%X\n", i, (int)blocks[i]);
  }
  // ... and the NULL-block again
  printf("Alloc block#%d: 0x%X\n", i, (int)mempool_alloc(port_pool));
  return 0;
}

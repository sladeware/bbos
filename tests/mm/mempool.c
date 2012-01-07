#include <bb/mm/mempool.h>
#include <bb/config/stdlib/stddef.h>
#include <bb/config/stdlib/stdio.h>
#include <string.h>

#define NR_BLOCKS 5
#define BLOCK_SZ 100 /* bytes */

MEMPOOL_PARTITION(part, NR_BLOCKS, BLOCK_SZ);

void
main()
{
  void* testpool;
  void* buf;
  int i;
  char ok = 0;

  testpool = mempool_init(part, NR_BLOCKS, BLOCK_SZ);

  for (i = 0; i < NR_BLOCKS; i++)
    {
      if (buf = mempool_alloc(testpool))
        ok++;
    }
  printf("OK: %d/%d\n", ok, NR_BLOCKS);

  if(buf == NULL)
    {
      printf("Cannot allocate new memory block from the pool.\n");
      return;
    }

  memcpy(buf, "Hello world!\0", 13);

  printf("%s", (char*)buf);
}

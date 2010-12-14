
#include <stdio.h>
#include <string.h>
#include <bbos/mm/ptsf.h>

char buf[80];

int main() {
  void *mypool;
  char *string = NULL;

  mypool = (void *)bbos_mempool_init((void *)buf, 80, 8);

  bbos_mempool_register(mypool, 8);

  string = bbos_malloc(8);
  printf("String <%p> -> <%p>\n", string, BBOS_CHUNK_PTR(void *, string));
  memcpy(PTSF_HANDLE(void *, string), "Hello", 5);
  printf("String: %s\n", PTSF_HANDLE(char *, string));

  return 0;
}


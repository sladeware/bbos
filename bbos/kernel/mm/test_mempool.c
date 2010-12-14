
#include <stdio.h>

#define BBOS_NUMBER_OF_MEMPOOLS 1

#include <bbos/mm/mempool.h>

char buf[100];

int main() {
	void *pool;
	char *string;
	
	printf("Pool <%p>\n", buf);
	pool = bbos_mempool_init((void *)buf, 100, 10);
	
	string = bbos_mempool_alloc(&pool);
	string = bbos_mempool_alloc(&pool);
	printf("String <%p>\n", string);
	
	
	return 0;
}



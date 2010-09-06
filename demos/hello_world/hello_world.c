
#include <bbos.h>

void
print_hello_world()
{
	printf("%s", "Hello world from the idle thread!\n");
	printf("%s", "Bye!\n");
	exit(0);
}

bbos_return_t
my_switcher(bbos_thread_id_t tid)
{
	switch(tid) {
		case BBOS_IDLE_THREAD_ID:
			print_hello_world();
			break;
  }
  return BBOS_SUCCESS;
}

int
main()
{
	bbos_init();

	bbos_start();

	return 0;
}



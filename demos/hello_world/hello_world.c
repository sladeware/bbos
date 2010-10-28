
#include <bbos.h>

void hello_world() {
  printf("Hello world!\n");
}

void bbos_application_init() {
  bbos_thread_init(HELLO_WORLD_ID, hello_world);
}

void bbos_application_exit() {

}



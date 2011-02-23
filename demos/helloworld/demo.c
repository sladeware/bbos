
#include <stdio.h>
#include <bbos/kernel.h>

void demo() {
	printf("Hello world!\n");
}

void main() {
	bbos_init();
	bbos_start_thread(DEMO, demo);
	bbos_start();
}


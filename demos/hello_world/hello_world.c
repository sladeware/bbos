
#include <bbos.h>

#pragma config \
	FPLLIDIV = DIV_2,  \
	FPLLMUL  = MUL_20, \
	FPLLODIV = DIV_1,  \
	FWDTEN   = OFF,    \
	POSCMOD  = XT,     \
	FNOSC    = PRIPLL, \
	FPBDIV   = DIV_2

#define DEG2RAD (M_PI / 180.0)

void bbos_main() {
  printf("Hello world!\n");
}


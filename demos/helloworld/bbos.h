/* Threads */
#define BBOS_NUMBER_OF_THREADS (2)
#define BBOS_IDLE (0)
#define HELLOWORLD (1)
/* Messages */
#define BBOS_NUMBER_OF_MESSAGES (3)
#define BBOS_DRIVER_INIT (0)
#define BBOS_DRIVER_CLOSE (1)
#define BBOS_DRIVER_OPEN (2)
/* Scheduling */
#define bbos_switch_thread()\
	while(1) {\
		helloworld();\
	}
/* Threads */
#define BBOS_NUMBER_OF_THREADS (2)
#define BBOS_IDLE (0)
#define HELLOWORLD (1)
/* Messages */
#define BBOS_NUMBER_OF_MESSAGES (3)
#define BBOS_DRIVER_INIT (0)
#define BBOS_DRIVER_CLOSE (1)
#define BBOS_DRIVER_OPEN (2)
/* Scheduling */
#define bbos_switch_thread()\
	while(1) {\
		helloworld();\
	}

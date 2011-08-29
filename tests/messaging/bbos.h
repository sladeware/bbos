
#define BBOS_ME "d2rk"

#define BBOS_CONFIG_PROCESSOR_NAME x86
#define BBOS_CONFIG_NR_THREADS 2
#define T0 0
#define T1 1

#define bbos_loop()\
  while (1) { \
    bbos_sched_jump(T0);\
    bbos_switch_thread();\
    bbos_sched_jump(T1);\
    bbos_switch_thread();\
  }

#define PING 0


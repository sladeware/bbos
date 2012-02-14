
#ifdef __CATALINA__
#include <catalina_icc.h>

#define bbos_delay_ticks(ticks) wait(ticks)
#define bbos_delay_msec(msec) msleep(msec)
#define bbos_delay_sec(sec) sleep(sec)

#else
#error Not supported compiler
#endif



#ifndef __BBOS_SCHEDULER_BASIC_POLICY_H
#define __BBOS_SCHEDULER_BASIC_POLICY_H

#ifdef __cplusplus
extern "C" {
#endif

/* Prototypes */

#define bbos_scheduler_suspend_thread(t) bbos_scheduler_remove_thread(t)
#define bbos_scheduler_resume_thread(t) bbos_scheduler_insert_thread(t)

void bbos_scheduler_init();

bbos_thread_id_t bbos_scheduler_get_next_thread();

bbos_return_t bbos_scheduler_insert_thread(bbos_thread_id_t tid);

bbos_return_t bbos_scheduler_remove_thread(bbos_thread_id_t tid);

bbos_thread_id_t bbos_scheduler_identify_thread();

#ifdef __cplusplus
}
#endif

#endif /* __BBOS_SCHEDULER_BASIC_POLICY_H */



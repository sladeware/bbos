/*
 * Copyright (c) 2011 Sladeware LLC
 */
#ifndef __BBOS_DRIVER_H
#define __BBOS_DRIVER_H

#define BBOS_DRIVER_FUNCTION_NAME(name, function)   \
  BB_JOIN2(name, function)

/* Get an access to driver's API */
#define BBOS_DRIVER_API(name, method, args)     \
  BBOS_DRIVER_FUNCTION_NAME(name, method) args

/* Get driver's prototype */
#define BBOS_DRIVER_PROTO(ret, name, method, args)  \
  ret BBOS_DRIVER_API(name, method, args)

/* Some well known functions */
#define BBOS_DRIVER_BOOTSTRAP(name) BBOS_DRIVER_API(name, bootstrap, ())
#define BBOS_DRIVER_RUNNER(name)    BBOS_DRIVER_API(name, runner, ())

#define BBOS_DRIVER_INTERFACE_PROTO(name)       \
  BBOS_DRIVER_PROTO(void, name, bootstrap, ()); \
  BBOS_DRIVER_PROTO(void, name, runner, ())

#ifdef BBOS_DRIVER

#if !defined(BBOS_DRIVER_TID) || BBOS_DRIVER_TID < 1
 #error "Thread identifier wasn't specified"
#endif

#if !defined(BBOS_DRIVER_PID)
 #define BBOS_DRIVER_PID 10
#endif /* BBOS_DRIVER_PID wasn't defined */

/* Get thread identifier */
#define bbos_driver_get_tid() (BBOS_DRIVER_TID)
#define bbos_driver_get_runner() BBOS_DRIVER_FUNCTION_NAME(BBOS_DRIVER, runner)
#define bbos_driver_get_port_id() (BBOS_DRIVER_PID)

void
BBOS_DRIVER_BOOTSTRAP(BBOS_DRIVER)
{
  bbos_thread_init(bbos_driver_get_tid(), bbos_driver_get_runner(),
                   bbos_driver_get_port_id());
#ifdef bootstrap_hook
  bootstrap_hook();
#endif
}


#endif /* BBOS_DRIVER */


#endif /* __BBOS_DRIVER_H */

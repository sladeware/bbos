
#ifndef __BBOS_HARDWARE_DEVICE_H
#define __BBOS_HARDWARE_DEVICE_H

typedef int16_t bbos_device_id_t;
typedef int8_t bbos_device_state_t;

struct bbos_device_vec {
  bbos_thread_id_t tid;
  int8_t *name;
  int16_t version;
  int8_t *config;
  void *private;
};

#ifndef BBOS_NUMBER_OF_DEVICES
#define BBOS_NUMBER_OF_DEVICES 0
#endif /* BBOS_NUMBER_OF_DEVICES */

/*
 * The number of devices can be equal to zero, but can not
 * be great than BBOS_MAX_NUMBER_OF_DEVICES.
 */
#if BBOS_NUMBER_OF_DEVICES > 0
extern struct bbos_device_vec bbos_device_table[BBOS_NUMBER_OF_DEVICES];
#endif /* BBOS_NUMBER_OF_DEVICES > 0 */

#if BBOS_NUMBER_OF_DEVICES > BBOS_MAX_NUMBER_OF_DEVICES
#error "BBOS_NUMBER_OF_DEVICES > BBOS_MAX_NUMBER_OF_DEVICES"
#endif

struct bbos_device {
  bbos_device_id_t id;
  bbos_device_id_t state_table[BBOS_NUMBER_OF_DEVICES];
};

/* Prototypes */


#endif /* __BBOS_HARDWARE_DEVICE_H */




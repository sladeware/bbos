
#ifndef __BBOS_HARDWARE_DEVICE_H
#define __BBOS_HARDWARE_DEVICE_H

typedef int16_t bbos_device_id_t;
typedef int8_t bbos_device_state_t;

struct bbos_device {
  bbos_device_id_t id;
  bbos_device_id_t state_table[BBOS_NUMBER_OF_DEVICES];
};

struct bbos_device_vec {
  bbos_thread_id_t tid;
  int8_t *name;
  int16_t version;
  int8_t *config;
  void *private;
};

extern struct bbos_device_vec bbos_device_table[BBOS_NUMBER_OF_DEVICES];

/* Prototypes */

bbos_return_t bbos_device_init(struct bbos_device *dev, bbos_device_id_t id);

bbos_return_t bbos_device_register(struct bbos_device *dev, bbos_thread_id_t tid, int8_t *name,
				   int16_t version, int8_t *config, void *private);

bbos_return_t bbos_device_unregister(struct bbos_device *dev);

bbos_return_t bbos_device_destroy(struct bbos_device *dev);

#endif /* __BBOS_HARDWARE_DEVICE_H */




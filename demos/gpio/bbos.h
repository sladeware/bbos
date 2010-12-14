
#ifndef __BBOS_H
#define __BBOS_H

// Threads
#define BBOS_DISABLE_SCHEDULER

// Ports
#define BLINKER_PORT_ID 0
#define GPIO_PORT_ID 1
#define BBOS_NUMBER_OF_PORTS 2

#define gpio_driver_init p8x32a_gpio_init
#define gpio_driver_messenger p8x32a_gpio_messenger

// Messages
enum {
	GPIO_OPEN,
	GPIO_CLOSE,
	GPIO_DIRECTION_INPUT, 
	GPIO_DIRECTION_OUTPUT,
	GPIO_SET_VALUE,
	GPIO_GET_VALUE
};

#endif


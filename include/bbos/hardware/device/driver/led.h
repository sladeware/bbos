/*
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#ifndef __HARDWARE_LED_H
#define __HARDWARE_LED_H

typedef enum {
	LED_OFF  = 0,
	LED_HALF = 127,
	LED_FULL = 255
} led_brightness_t;

struct led_info {
};

struct led_platform_data {
	uin16_t num_leds;
	struct led_info *leds;
};

struct gpio_led_info {
	uint16_t gpio;
};

struct gpio_led_platform_data {
	uint16_t num_leds;
	struct gpio_led *leds;
};

#endif /* __HARDWARE_LED_H */


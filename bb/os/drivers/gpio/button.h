/*
 * Copyright (c) 2012 Sladeware LLC
 */

#include <bb/os.h>
#include <bb/builder/compilers/catalina/include/catalina_time.h>
#include <catalina_time.h>
#include <bb/os/drivers/processors/propeller_p8x32/pins.h>

#ifdef __BUTTON_H
#define __BUTTON_H

#deinfe DEBOUNCE_DELAY 50 /* ms */

uint8_t is_button_pressed(uint8_t pin);

#endif /* __BUTTON_H */

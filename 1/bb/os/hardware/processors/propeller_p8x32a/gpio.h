
#ifndef __GPIO_H
#define __GPIO_H

#ifndef __CATALINA__
#error ""Unsupported compiler
#endif

#include <catalina_cog.h>

#define GET_PIN(pin) (1<<(pin))

#define GPIOA_SET_HIGH(pin) _outa(GET_PIN(pin), GET_PIN(pin))
#define GPIOA_SET_LOW(pin) _outa(GET_PIN(pin), 0)
#define GPIOA_SET_INPUT(pin) _dira(GET_PIN(pin), 0)
#define GPIOA_SET_OUTPUT(pin) _dira(GET_PIN(pin), GET_PIN(pin))
#define GPIOA_GET_STATE(pin) (!!(_ina() & GET_PIN(pin)))

#define GPIOA_SET_GROUP_OUTPUT(first, last) _dira(GET_PIN((last)+1) - GET_PIN(first), GET_PIN((last)+1) - GET_PIN(first))

#endif


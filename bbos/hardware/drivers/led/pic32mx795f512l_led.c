
#include <bbos/hardware/drivers/hal.h>

#ifndef PIC32MX795F512L_LED_DRIVER_ID
#error "PIC32MX795F512L_LED_DRIVER_ID identifier was not defined"
#endif

static bbos_return_t
bbos_driver_command()
{
}

void
pic32mx795f512l_led_init() {
  bbos_thread_init(PIC32MX795F512L_LED_DRIVER_ID, bbos_driver_messenger);
  bbos_scheduler_insert_thread(PIC32MX795F512L_LED_DRIVER_ID);
}



// Blinker thread

#include <bb/os.h>
#include BBOS_PROCESSOR_FILE(pins.h)
#include BBOS_PROCESSOR_FILE(delay.h)

#define LED_PIN 20
#define MASK (1 << LED_PIN)
static int8_t led_state = 0;

void blinker_runner() {
  DIR_TO(LED_PIN, led_state);
  OUT_TO(LED_PIN, led_state);
  led_state ^= 1;
  bbos_delay_sec(1);
}

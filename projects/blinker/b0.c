// B0 thread

#include <bb/os.h>
#include BBOS_PROCESSOR_FILE(pins.h)
#include BBOS_PROCESSOR_FILE(delay.h)

static int8_t led_state = 0;

void b0_runner() {
  DIR_TO(16 + cogid(), led_state);
  OUT_TO(16 + cogid(), led_state);
  led_state ^= 1;
  bbos_delay_sec(1);
}

// Blinker thread

#include <bb/os.h>
#include BBOS_PROCESSOR_FILE(pins.h)

void blinker_runner() {
  DIR_OUTPUT(20);
  OUT_HIGH(20);
}

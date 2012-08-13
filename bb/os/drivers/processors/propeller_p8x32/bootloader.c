// Copyright (c) 2012 Sladeware LLC
// Author: Oleksandr Sviridenko

#include <propeller.h>
#include "bb/os/drivers/processors/propeller_p8x32/sio.h"

// Configurable definitions
#define BOOTLOADER_BANNER 0
#define DEBUG
#define COMMAND_TIMEOUT 2 // seconds
#define MAX_NR_IMAGES 8

// Internal definitions
//#define bbos_get_byte() sio_get_char()
#define bbos_wait_byte_with_timeout(sec) sio_wait_byte_with_timeout(sec)

#ifdef DEBUG
#define DEBUG_PRINTF(frmt, ...) sio_printf(frmt, __VA_ARGS__)
#endif

static int16_t nr_images = 0;
// This array keeps the address of images assigned by an index
static int16_t image_addresses[MAX_NR_IMAGES];

static void start()
{
  char cmd;
  int16_t i;

  // First of all, initialize serial I/O
  sio_init();

#if BOOTLOADER_BANNER
  sio_printf(" ____ ____     ____          _   _              _    \r\n");
  sio_printf("| __ ) __ )   | __ ) __  __ | |_| | __  __ _ __| |   \r\n");
  sio_printf("|  _ \\  _ \\   |  _ \\/  \\/  \\| __/ |/  \\/ _` | _` |\r\n");
  sio_printf("|  _) ) _) )  |  _) ) ) ) ) | |_| |  ) )(_| |(_| |   \r\n");
  sio_printf("|____/____/   |____/\\__/\\__/ \\__|_|\\__/\\__,_|__,_|\r\n");
#endif // BOOTLOADER_BANNER

  // Initialization ...
  // ... clear map of image addresses
  for (i = 0; i < MAX_NR_IMAGES; i++) {
    image_addresses[i] = -1;
  }
  // Wait for number of images to be read
  if (!(nr_images = bbos_wait_byte_with_timeout(COMMAND_TIMEOUT))) {
    return;
  }
  DEBUG_PRINTF("Number of images: %d\n", nr_images);

  // Start reading required number of images
  for (i = 0; i < nr_images; i++) {

  }

#if 0
  // wait for a command
  while (1) {
    cmd = bbos_wait_byte_with_timeout(3);
    if (!cmd) {
      DEBUG_PRINTF("Timeout %d!\r\n", 3);
      return;
    }
    DEBUG_PRINTF("Command '%d', char '%c'\r\n", cmd, cmd);
  }
#endif
}

static void stop()
{
}

int main(void)
{
  start();
  return 0;
}

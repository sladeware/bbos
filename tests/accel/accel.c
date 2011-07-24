/*
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

#include <bb/os/kernel/system.h>
#include <bb/os/hardware/drivers/accel/h48c/core.h>

static struct h48c_pins demo_pins = {1, 2, 0, 3};
static bool_t init_complete = 0;
static int is_free_fall;

void
freefall_runner()
{
  static bbos_message_t message; // message to communicate with accelerometer

  // Demo has a new message
  if (bbos_port_receive(FREEFALL, &message) == BBOS_SUCCESS)
    {
      // Try to figure out the command
      switch (message.id)
	{
	case BBOS_DRIVER_OPEN:
	  printf("H48C device has been opened\n");
	  init_complete = 1;
	  break;
	  // Response from the free fall detection
	case H48C_FREEFALL:
	  if (*(int *)message.data == 1)
	    printf("Free fall detected!\n");
	  break;
	default:
	  bbos_panic("Unknown message");
	  break;
	}
    }

  if (!init_complete)
    {
      printf("Send open-message to H48C device driver\n");
      message.id = BBOS_DRIVER_OPEN;
      message.data = &demo_pins;
      bbos_port_send(H48C, &message, DEMO);
      return;
    }

  message.id = H48C_FREE_FALL;
  message.data = &is_free_fall;
  bbos_port_send(H48C, &message, DEMO);
}

int
main()
{
  bbos_init();
  bbos_add_thread(FREEFALL, freefall_runner);
  bbos_add_thread(H48C, h48c_runner);
  bbos_start();

	return 0;
}


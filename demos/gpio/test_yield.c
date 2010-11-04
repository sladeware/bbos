/*
 * The test aims to get basic skills of using GPIO driver.
 *
 * Meantime, from this sample you will know how to use one port to keep a 
 * messages with the different footprint from different senders.
 *
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

#include <bbos.h>
#include <bbos/hardware/drivers/gpio/p8x32a.h>

// Port for 10 driver messages.
#define TEST_PORT_NUMBER_OF_MESSAGES 10
#define TEST_PORT_SIZE (TEST_PORT_NUMBER_OF_MESSAGES * \
	sizeof(struct bbos_driver_response))
char test_port[TEST_PORT_SIZE];

unsigned int pin = 1;
unsigned int mask = 1 << 1;
unsigned int indicator = 1 << 1;

char xinit_complete = 0;
char init_complete = 0;

struct bbos_gpio_message gpio_message;

void bbos_main() {
  struct bbos_driver_request gpio_request;
  struct bbos_driver_response gpio_response;

  sleep(1);

  /* Initialize test */
  if (!xinit_complete) {
    bbos_port_init(TEST_PORT_ID, test_port, TEST_PORT_SIZE);

    /* Initialize GPIO driver */
#if !defined(BBOS_PROCESSOR)
#error "Processor was not set"
#elif BBOS_PROCESSOR == P8X32A
#define BBOS_GPIO_DRIVER_ID P8X32A_GPIO_ID 
    p8x32a_gpio_init();
#else
#error "We do not have a support of GPIO for this processor."
#endif

    xinit_complete = 1;
    printf("Test initialization... done.\n");
  }

  //while (1) {
  /* Do we have a new message to process? */
  if (!bbos_port_empty(TEST_PORT_ID)) {
    /* 
     * Get the message sender first; thus we can define its owner and the 
     * message structure.
     */
    bbos_port_read(TEST_PORT_ID, &gpio_response, sizeof(gpio_response));
    
    /* Go throw senders to get the rest of the message */
    switch (gpio_response.sender) {
    case BBOS_GPIO_DRIVER_ID:
      
      printf("Received a new message from GPIO driver.\n");
      
      /* Process response to previously required commands */
      switch (gpio_response.command) {
      case BBOS_GPIO_OPEN:
	if (gpio_response.error == BBOS_SUCCESS) {
	  printf("Required pin was successfully owned.\n");
	} else {
	  printf("Cannot open required pin: %d\n", gpio_response.error);
	}
	/* Main thread owns GPIO driver control */
	init_complete = 1;
	break;
      case BBOS_GPIO_DIRECTION_OUTPUT:
	if (gpio_response.error == BBOS_SUCCESS) {
	  printf("Output direction was set.\n");
	} else {
	  printf("Cannot set output: %d\n", gpio_response.error);
	  return;
	}
	break;
      }
      break;
				
    default:
      printf("Unknown sender: %d\n", gpio_response.sender);
      break;
    }
  }
		
  /*
   * Initialize GPIO driver. Send a message with BBOS_DRIVER_OPEN command to the
   * GPIO driver and wait for its response.
   */
  if (!init_complete) {
    gpio_request.sender = BBOS_MAIN_ID;
    gpio_request.command = BBOS_GPIO_OPEN;
    gpio_message.pin = pin;
    gpio_message.value = indicator;
    gpio_request.output = TEST_PORT_ID;		
    gpio_request.data = &gpio_message;
    bbos_port_write(P8X32A_GPIO_PORT_ID, &gpio_request, sizeof(gpio_request));
    //bbos_thread_yield();
    //continue;
    printf("Sent message to GPIO driver to open pin %d.\n", pin);
    return;
  }
	
  /*
   * Form request for blink :)
   */
  printf("Sent message to GPIO driver to set output direction\n");
  gpio_request.sender = BBOS_MAIN_ID;
  gpio_request.command = BBOS_GPIO_DIRECTION_OUTPUT;
  gpio_request.output = TEST_PORT_ID;		
  gpio_message.pin = pin;
  gpio_message.value = indicator;
  indicator ^= mask; // turn on or turn off desired pin
  gpio_request.data = &gpio_message;
  gpio_request.size = sizeof(struct bbos_gpio_message);
  bbos_port_write(P8X32A_GPIO_PORT_ID, &gpio_request, sizeof(gpio_request));

  //bbos_thread_yield();
  //}
}






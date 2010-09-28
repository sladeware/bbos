
#include <bbos.h>
#include <bbos/hardware/driver/gpio.h>

struct bbos_driver_message message;
int offset;

void
test()
{
  offset = 0x1;

	message.driver_id = PARALLAX_GPIO_DRIVER_ID;
	message.cmd = GPIO_DIRECTIO_INPUT;
  message.private = &offset;

  bbos_itc_send(GPIO_DRIVER_THREAD_ID, &message);
}

int main() {
	bbos_init();

	// Start thread related with GPIO driver
	bbos_thread_start(GPIO_DRIVER_THREAD_ID, BBOS_THREAD_LOWEST_PRIORITY);

	// Register supported GPIO drivers. All the GPIO drivers related to 
	// GPIO_DRIVER_THREAD_ID thread.
  struct gpio_info parallax_gpio;
  parallax_gpio.labal = "GPIOA";
  parallax_gpio.base = 0;
  parallax_gpio.n = 32;
  parallax_gpio.bitmap = 0x0;
	bbos_driver_register(PARALLAX_GPIO_DRIVER_ID, GPIO_DRIVER_THREAD_ID, 
    "PARALLAX/GPIO", 1, &parallax_gpio);

	bbos_thread_start(TEST, BBOS_THREAD_LOWEST_PRIORITY);

	// Send a message to open PRALLAX/GPIO driver
	message.driver_id = PARALLAX_GPIO_DRIVER_ID;
	message.cmd = BBOS_DRIVER_CMD_OPEN;
	bbos_itc_send(GPIO_DRIVER_THREAD_ID, &message);

	bbos_start();

	return 0;
}

